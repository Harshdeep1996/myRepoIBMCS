import re
import os
import git
import tempfile
import shutil
import time
import logging
from collections import namedtuple
from datetime import datetime as dt


evidence_params = ['name', 'url', 'ttl', 'description']
Evidence = namedtuple('Evidence', evidence_params)
evidence_params.append('fetch_function')
FetchableEvidence = namedtuple('Evidence', evidence_params)

FORMAT = '%(asctime)-15s locker:%(name)s %(message)s'
logging.basicConfig(format=FORMAT)


class Locker:
    """
    The evidence Locker maintains a git repo of evidence and places new
    evidence into it. It can validate a piece of evidence against a TTL.

    The Locker is a context manager. On instantiation it will retrieve the
    configured git repository
    """

    def __init__(self, repo_dir='example', repo_url=None, branch='master',
                 config=None):
        """
        Create a Locker.v

        :param repo_url: the URL of a git repository, credentials are supplied
            via envvars. If not set, create a local repo and commit without
            pushing to a remote.
        :param repo_dir: directory name (not path) to create a git repo in, if
            a url is not specified.
        :param branch: branch of the repo, defaults to master, only used if
            repo is cloned from repo_url.

        """
        if config is not None:
            repo_url = re.sub(
                '://', '{}{}{}'.format('://', config['github'].token, '@'),
                repo_url)
        self.repo_url = repo_url
        self.branch = branch
        if repo_url:
            self.repo_dir = os.path.split(self.repo_url)[1]
        elif repo_dir:
            self.repo_dir = repo_dir
        else:
            raise UnboundLocalError('need one of repo_dir or repo_url')
        self.repo_path = os.path.join(tempfile.gettempdir(), self.repo_dir)
        self.logger = logging.getLogger(name=self.repo_dir)
        self.touched_files = []

    def add(self, filepath):
        """
        Add the requested file to the locker. This means checking the file
        into the lockers git repository.

        :param filepath: the path to a file to be written into the locker
        """
        logging.info('adding file {} to {}'.format(
            filepath,
            self.repo.git_dir
        ))
        shutil.copy(filepath, os.path.split(self.repo.git_dir)[0])

        self.index(filepath)

    def index(self, filepath):
        self.touched_files.append(filepath)
        self.repo.index.add([os.path.split(filepath)[1]])

    def repo_init(self):
        """
        Create an empty git repo
        """
        local_repo_dir = self.repo_path
        self.repo = git.Repo.init(local_repo_dir)

    def get_file(self, filename):
        """
        Get the path for a file in the locker, which may or may not exist

        :param filename: the name of a file in the locker
        """
        return os.path.join(self.repo_path, filename)

    def validate(self, evidence, with_github=False):
        """
        Validate the evidence against the ttl

        :param evidence: an Evidence namedtuple
        :param with_github: Verification to be done with github or not
        """
        try:
            if with_github is True:
                g = git.Git(self.repo_path)
                file_age = dt.strptime(g.log('-1', '--pretty="%cI"',
                                             evidence.name)[1:-7],
                                       "%Y-%m-%dT%H:%M:%S")
                if (dt.now() - file_age).total_seconds() > evidence.ttl:
                    self.logger.error('{} failed ttl validation github {} > {}'
                                      .format(evidence.name,
                                              dt.now() - file_age,
                                              evidence.ttl))
                    return False
                return True
            else:
                file_path = self.get_file(evidence.name)
                mtime = os.path.getmtime(file_path)
                self.logger.info('{} last modified {}'.format(
                    evidence,
                    time.ctime(mtime))
                )
                # passes validation if the time delta is less than the ttl
                now = time.time()
                if now - mtime > evidence.ttl:
                    self.logger.error('{}failed ttl validation locally {} > {}'
                                      .format(evidence.name,
                                              now - mtime,
                                              evidence.ttl))
                return now - mtime < evidence.ttl
        except Exception as e:
            self.logger.error('{} failed validation with error: {}'.format(
                evidence.name,
                e.message
            ))
            return False

    def checkout(self):
        """
        Pull (clone) the remote repository to the local
        """
        self.repo = git.Repo.clone_from(
            self.repo_url,
            self.repo_path,
            branch=self.branch
        )

    def checkin(self):
        """
        Commit changed files to the local repository
        """
        message = 'update documents {}\n\n{}'.format(
            time.ctime(time.time()),
            '\n'.join([os.path.basename(f) for f in self.touched_files])
        )

        try:
            diff = self.repo.index.diff('HEAD')
            if len(diff) + len(self.touched_files) > 0:
                self.repo.index.commit(message)
        except git.BadName:
            self.repo.index.commit(message)

    def delete_repo_locally(self):
        """
        Deletes the repo if working locally and will ignore if not locally.
        """
        try:
            shutil.rmtree(self.repo_path)
        except OSError:
            pass

    def push(self):
        """
        Push the repository to the remote
        """
        self.repo.remotes[0].push()

    def __enter__(self):
        """
        Either check out the repository from `repo_url` or create a local one
        """
        if self.repo_url:
            self.checkout()
        else:
            self.repo_init()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Log the exception if raised, commit the files to the repo and if
        configured push it up to the `repo_url`.
        """
        if exc_type:
            self.logger.error(' '.join([str(exc_type), str(exc_val)]))
        self.checkin()
        if self.repo_url:
            self.push()
        return
