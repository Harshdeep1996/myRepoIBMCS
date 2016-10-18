import unittest
from compliance.utils.evidence import Locker
from compliance.utils.workflow import Workflow


class TestTemplate(unittest.TestCase):

    repo = 'https://github.ibm.com/cloudant/evidence-collector'

    @classmethod
    def setUpClass(cls):
        with Locker(repo_url=cls.repo, config=cls.config) as locker:
            cls.locker = locker
            cls.case = Workflow(cls.locker)

    @classmethod
    def tearDownClass(cls):
        failed = cls.case.validate_and_fetch()
        cls.case.closed = True
        assert cls.case.passes()
        cls.locker.checkin()
        cls.locker.push()
        cls.locker.delete_repo_locally()
