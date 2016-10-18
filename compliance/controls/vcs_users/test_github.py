import os
import json
import unittest
from utilitarian.credentials import Config
from compliance.utils.evidence import Locker
from compliance.utils.workflow import Workflow


class TestGithubUserAccess(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Fetch the evidence and verify based on TTL. Keep the locker around for
        use in more detailed tests.
        """
        json_file = 'test_github_users.json'
        dir_tuple = os.path.split(os.path.abspath(__file__))
        cls.test_def = json.load(open('{}{}{}'.format(dir_tuple[0],
                                                      '/', json_file)))
        config = Config('~/.credentials')
        with Locker(repo_url=cls.test_def['repo'], config=config) as locker:
            cls.locker = locker
            case = Workflow(cls.locker)
            failed = case.validate_and_fetch()
            assert case.passes()

    def test_github_users(self):
        """
        Verify that the list of users in github is the same as the expected
        list from USAM.
        """
        usam_users = json.load(
            open(self.locker.get_file('usam_users.json'))
        )
        github_users = json.load(
            open(self.locker.get_file('github_users.json'))
        )

        assert set(usam_users) - set(github_users) == set()

    def test_github_emails(self):
        """
        Verify that people are only using ibm.com email addresses
        """
        github_users = json.load(
            open(self.locker.get_file('github_users.json'))
        )
        failed_users = []
        for user in github_users:
            if not user['email'].endswith('ibm.com'):
                failed_users.append(user)
        assert len(failed_users) == 0
