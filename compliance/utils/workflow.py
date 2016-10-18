import os
import logging
from utilitarian.services.tickets import connect_to_fogbugz, ticket
from utilitarian.credentials import Config
from compliance.utils.fetch import fetch
from compliance.utils.evidence import Evidence, Locker
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta


FORMAT = '%(asctime)-15s locker:%(name)s %(message)s'
logging.basicConfig(format=FORMAT)


class Workflow(object):
    """
    A Workflow knows how to get Evidence into its locker and validate it.
    """

    def __init__(self, locker):
        self.locker = locker
        self.id = 0
        self.logger = self.locker.logger.getChild('{}'.format(self.id))
        self.evidence = []

    def required_evidence(self, list_of_evidence=[]):
        self.evidence = list_of_evidence

    def validate_and_fetch(self):
        """
        Retrieve a piece of evidence and place it in the locker. This may come
        from a URL or an attachment on the FB case.
        """
        failed = []
        # Go through all the evidences that satisfy the check
        invalid_evidences = filter(
            lambda x: not self.locker.validate(x),
            self.evidence
        )
        for evidence in invalid_evidences:
            # The evidence either doesn't exist or is out of ttl
            try:
                self.collect(evidence)
            except:
                # Something went wrong
                failed.append(evidence)
        return failed

    def passes(self, report=False):
        """
        Does the Workflow pass all validation? Is the case
        closed?
        """
        failed = self.validate_and_fetch()
        if report:
            self._report(failed)
        return len(failed) == 0

    def _report(self, failed):
        """
        Write a file with a report of failures
        """
        pass

    def collect(self, evidence):
        """
        collect retrieves the evidence, either by calling the evidences
        fetch_function or by using fetch()
        """
        if evidence.fetch_function:
            self.locker.add(evidence.fetch_function(evidence))
        elif evidence.url:
            # Can just retrieve the file and place in the locker
            self.locker.add(fetch(evidence.url))


class FogbugzCaseWorkflow(Workflow):
    """
    A CaseWorkflow is responsible for interacting with the ticketing system
    to open and update cases, and store the case and any attachments into the
    evidence locker.

    The workflow has 4 states:

    state 1: nothing in the locker - action, open case, put case.xml in the
    locker, fail

    state 2: only case.xml in locker - action, retrieve case & attachments,
    update locker, fail if case is open, fail if attachments are out of ttl

    state 3: case.xml & attachments in locker, attachments in ttl - action,
    retrieve case, fail if case is open, return success if closed

    state 4: case.xml & attachments in locker, attachments out of ttl -
    action, retrieve case & attachments, fail if case is open, if
    attachments are still out of ttl, return success otherwise
    """

    def __init__(self, locker, init_case={}, interval=None):
        super(FogbugzCaseWorkflow, self).__init__(locker)
        self.closed = False
        config = Config('~/.credentials')
        self._fb = connect_to_fogbugz(creds=config)
        if not os.path.exists(self.locker.get_file('case.xml')):
            self._create_case(init_case)
        else:
            self._load_xml()
            if interval is not None:
                self.checking_date(init_case, interval)
        self.retrieve()
        self.logger = self.locker.logger.getChild('{}'.format(self.id))

    def checking_date(self, init_case, interval):
        '''
        For both automated and non automated cases, it makes the a new ticket
        after a certain interval of time.

        Eg: Nessus scan needs to be done weekly, so it takes Fogbugz ticket
        creation date and creates a ticket weekly
        '''
        with open(self.locker.get_file('case.xml'), 'r') as casefile:
            soup = BeautifulSoup(casefile.read())
            dt_from_case = soup.response.case.dt.getText()
        # Because Fogbugz believes in GMT
        date_opened = (
            datetime.strptime(
                dt_from_case,
                "%Y-%m-%dT%H:%M:%SZ") +
            timedelta(minutes=60))
        if datetime.now() >= date_opened + timedelta(minutes=interval):
            self._create_case(init_case)

    def _create_case(self, init_case):
        self._write_xml(ticket(self._fb, case=init_case))
        self._load_xml()

    def _load_xml(self):
        with open(self.locker.get_file('case.xml'), 'r') as casefile:
            soup = BeautifulSoup(casefile.read())
            self.id = int(soup.response.case['ixbug'])
            self.closed = soup.response.case.fopen
            # TODO: track date of close event

    def _write_xml(self, data):
        """
        Write the data into case.xml and add it to the locker
        """
        with open(self.locker.get_file('case.xml'), 'w') as casefile:
            casefile.write(str(data))
            self.locker.index(self.locker.get_file('case.xml'))

    def retrieve(self):
        """
        Retrieve the case (updating case.xml in the locker) and events and
        store any attachments on the case in the locker.
        """
        fields = ["ixBug", "sTitle", "fOpen", "events"]
        # TODO: create new case is self.id == 0 & update id to point to it
        case = self._fb.search(q=self.id, cols=','.join(fields))
        self._write_xml(case.prettify('utf8'))
        # Build up a dictionary tracking the files on the case and the URL that
        # hosts the file.
        evidences_from_case = []
        if hasattr(case, 'events'):
            for e in case.events.childGenerator():
                for a in e.rgattachments.childGenerator():
                    base_url = os.path.split(getattr(self._fb, '_url'))[0]
                    e = Evidence(
                        name=a.sfilename.string,
                        url=os.path.join(
                            base_url,
                            a.surl.string.replace('&amp;', '&')
                        ),
                        ttl=0,
                        description='file from case {}'.format(self.id)
                    )
                    evidences_from_case = e
        self.logger.info('has {} files attached to case {}'.format(
            len(evidences_from_case), self.id)
        )
        # Now retrieve the attached files - if there are any files attached
        # to the case
        if len(evidences_from_case) is not 0:
            self.collect(evidences_from_case)

    def passes(self, report=False):
        """
        Does the Workflow pass all validation? Is the case
        closed?
        """
        failed = self.validate_and_fetch()
        if report:
            self._report(failed)
        return self.closed and len(failed) == 0


def run_evidence_collection(test_def=[], repository=None):
    with Locker(repository) as locker:
        cases = FogbugzCaseWorkflow(locker)
        # Read the case.xml (if one exists) and get attachmetns, or create a
        # new case if it doesn't
        cases.retrieve()
        failed = cases.validate_and_fetch(
            [Evidence(**x) for x in test_def]
        )

        if not failed:
            assert cases.passes()
        # Can also be called as:
        # assert cases.passes(report=True)
        # assert cases.passes(report=True,
        #  list_of_evidence=[Evidence(**x) for x in test_def])
