import tempfile
import shutil
import os

from collections import defaultdict
from nose import with_setup
from nose.tools import assert_true, assert_false, assert_equals, assert_in

from mock import patch, MagicMock

from compliance.utils.evidence import Locker, Evidence
from compliance.utils.fetch import fetch
# from compliance.utils.workflow import run_evidence_collection


REPO_DIR = 'test_locker_repo'
FILES_DIR = os.path.join(tempfile.gettempdir(), 'test_locker_files')


def setup_temp():
    clean_temp()
    os.mkdir(FILES_DIR)
    os.mkdir(os.path.join(tempfile.gettempdir(), REPO_DIR))


def clean_temp():
    shutil.rmtree(os.path.join(tempfile.gettempdir(), REPO_DIR), ignore_errors=True)
    shutil.rmtree(FILES_DIR, ignore_errors=True)


def test_repo_dir():
    """
    Test that different URLs set repo_dir properly
    """
    examples = [
        'https://user:pass@github.com/cloudant/test.git',
        'https://github.com/cloudant/test.git',
        'git@github.com:cloudant/test.git'
    ]
    for url in examples:
        locker = Locker(repo_url=url)
        assert_equals(locker.repo_dir, 'test.git')


@patch('git.Repo')
def test_clone(git_mock):
    """
    Test that clone is called when URL is provided
    """
    url = 'git@github.ibm.com:simonmetson/locker-demo.git'
    locker = Locker(repo_url=url)
    locker.checkout()
    git_mock.clone_from.assert_called_with(
        url, os.path.join(tempfile.gettempdir(), 'locker-demo.git'), branch='master'
    )


@with_setup(setup_temp)
def test_add_locally():
    """
    Test putting files into the locker (no URL provided)
    """
    with Locker(repo_dir=REPO_DIR) as locker:
        f = tempfile.mkstemp(
            prefix='testfile', suffix='.tmp', dir=FILES_DIR,
        )
        locker.add(f[1])

        filename = os.path.basename(f[1])
        assert_true(os.path.isfile(os.path.join(tempfile.gettempdir(), REPO_DIR, filename)))
        assert_true(locker.repo.is_dirty())
        assert_equals(len(locker.repo.index.entries), 1)
        assert_in((filename, 0), locker.repo.index.entries.keys())

    assert_false(locker.repo.is_dirty())
    commit = next(locker.repo.iter_commits())
    assert_in('update documents', commit.message)
    assert_in(filename, commit.message)


@with_setup(setup_temp)
@patch('git.Repo')
def test_add_with_url(git_mock):
    """
    Test putting files into the locker with URL (clone/push must be called)
    """
    url = 'https://test:pass@github.ibm.com/cloudant/test.git'
    repo_mock = MagicMock()
    repo_mock.git_dir = os.path.join(tempfile.gettempdir(), REPO_DIR)
    repo_mock.remotes = [repo_mock]
    git_mock.clone_from.return_value = repo_mock
    with Locker(repo_dir=REPO_DIR, repo_url=url) as locker:
        f = tempfile.mkstemp(
            prefix='testfile', suffix='.tmp', dir=FILES_DIR,
        )
        locker.add(f[1])

    repo_mock.push.assert_called_once()


@with_setup(setup_temp)
def test_add_locally_identical():
    """
    Test putting two identical files into the locker
    """

    tmp_file = tempfile.mkstemp(
        prefix='testfile', suffix='.tmp', dir=FILES_DIR
    )[1]
    tmp_basename = os.path.basename(tmp_file)

    with Locker(repo_dir=REPO_DIR) as locker:
        locker.add(tmp_file)
        assert_true(os.path.isfile(
            os.path.join(tempfile.gettempdir(), REPO_DIR, tmp_basename))
        )

    commits = [c for c in locker.repo.iter_commits()]
    assert_equals(len(commits), 1)

    with Locker(repo_dir=REPO_DIR) as locker:
        locker.add(tmp_file)
        assert_true(os.path.isfile(
            os.path.join(tempfile.gettempdir(), REPO_DIR, tmp_basename))
        )

    commits = [c for c in locker.repo.iter_commits()]
    assert_equals(len(commits), 2)
    assert_true(all([tmp_basename in c.message for c in commits]))


@with_setup(setup_temp)
def test_add_locally_multiple():
    """
    Test putting files into the locker (no URL provided)
    """

    filenames = []
    with Locker(repo_dir=REPO_DIR) as locker:
        for i in range(4):
            f = tempfile.mkstemp(
                prefix='testfile', suffix='.{}.tmp'.format(i), dir=FILES_DIR
            )
            locker.add(f[1])

            filename = os.path.basename(f[1])
            assert_true(os.path.isfile(
                os.path.join(tempfile.gettempdir(), REPO_DIR, filename))
            )
            assert_true(locker.repo.is_dirty())
            assert_equals(len(locker.repo.index.entries), i + 1)
            assert_in((filename, 0), locker.repo.index.entries.keys())
            filenames.append(filename)

    assert_false(locker.repo.is_dirty())
    commits = [c for c in locker.repo.iter_commits()]
    assert_equals(len(commits), 1)
    assert_true(all([x in commits[0].message for x in filenames]))


@with_setup(setup_temp)
def test_fetch_and_add():
    '''
    Test fetch a file and add it into the locker
    '''
    e = Evidence(
        'logo.svg',
        'https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg',
        2592000,
        'IBM Logo'
    )
    check = defaultdict(list)
    with Locker(repo_dir=REPO_DIR) as locker:
        assert_false(locker.validate(e))
        try:
            locker.add(fetch(e))
        except:
            check['failed'].append(e.name)
    assert_equals(len(check['failed']), 0)


#### TODO: tests to be implemented/fixed

# @with_setup(setup_temp)
# @patch('git.Repo')
# def test_clone_fetch_and_add(git_mock):
#     '''
#     Test clone repo, fetch a file, add and push it into the locker
#     '''
#     url = 'git@github.ibm.com:simonmetson/locker-demo.git'
#     e = Evidence(
#         'logo.svg',
#         'https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg',
#         2592000,
#         'IBM Logo'
#     )

#     repo_mock = MagicMock()
#     repo_mock.git_dir = '/tmp/' + REPO_DIR
#     repo_mock.remotes = [repo_mock]
#     git_mock.clone_from.return_value = repo_mock

#     with Locker(repo_url=url) as locker:
#         git_mock.clone_from.assert_called_with(
#             url, '/tmp/locker-demo.git', branch='master'
#         )
#         assert_false(locker.validate(e))
#         locker.add(fetch(e))

#     repo_mock.push.assert_called_once()


# def testExample():
#     """
#     Some dream code
#     """
#     test_def = [
#         {
#             name: 'my_policy.pdf',
#             url: 'http://example.com/my_policy.pdf',
#             ttl: 1234,
#             description: 'policy about VCS access'
#         },
#         {
#             name: 'users_list.pdf',
#             url: None,
#             ttl: 1234,
#             description: 'users with access to Cloudant VCS (github.com)'
#         }
#     ]
#     run_evidence_collection(test_def)
