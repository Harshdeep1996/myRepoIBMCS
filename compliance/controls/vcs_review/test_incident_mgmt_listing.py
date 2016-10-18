import os
import unittest
import unicodecsv as csv
from collections import namedtuple
from datetime import datetime, timedelta
from utilitarian.credentials import Config
from compliance.utils.evidence import Evidence
from compliance.utils.test_template import TestTemplate
from utilitarian.services.tickets import search, connect_to_fogbugz


class TestFogbugzIncidentMgmt(TestTemplate):

    config = Config(os.path.expanduser('~/.credentials'))

    def fb_incident_mgmt_listing(self):
        fb = connect_to_fogbugz(creds=self.config)
        im_list = []
        criteria = ['ID',
                    'Title',
                    'Category',
                    'Priority',
                    'Environment',
                    'Date_Opened',
                    'Date_Closed',
                    'Status']
        fields = ["ixBug", "sTitle",
                  "sCategory", "ixPriority",
                  "sArea", "sProject",
                  "dtOpened", "fOpen", "dtClosed"]

        Attributes = namedtuple('Attributes', criteria)

        # Generic period of 4 months taken into consideration
        period_of_tickets = str((datetime.now() -
                                timedelta(minutes=120 * 24 * 60)).date())
        query = 'opened:"%s..now"' % period_of_tickets
        response = search(fb, fields=fields, query=query)

        for case in response.cases:
            im_list.append(Attributes(
                        case['ixbug'], case.stitle.getText(),
                        case.scategory.getText(), case.ixpriority.string,
                        case.sarea.string + " : " + case.sproject.string,
                        case.dtopened.string, case.dtclosed.string,
                        case.fopen.string))

        with open('output_im_listing.csv', 'w') as f:
            w = csv.writer(f, encoding='utf-8')
            w.writerow(tuple(criteria))
            w.writerows([(data.ID,
                          data.Title,
                          data.Category,
                          data.Priority,
                          data.Environment,
                          data.Date_Opened,
                          data.Date_Closed,
                          data.Status) for data in im_list])

    def test_validate(self):
        evidence = Evidence(
                'output_im_listing.csv', None, 82800,
                'All tickets created on Fogbugz within a specific period.')
        try:
            assert self.locker.validate(evidence, with_github=True)
        except AssertionError:
            self.fb_incident_mgmt_listing()
            self.locker.add(evidence.name)

if __name__ == '__main__':
    unittest.main()
