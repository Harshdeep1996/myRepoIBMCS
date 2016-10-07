import os
from travispy import TravisPy
from utilitarian.credentials import Config

creds = Config(os.path.expanduser('~/.credentials'))

t = TravisPy.github_auth(creds['github'].token)

repo = t.repo('Harshdeep1996/myRepoIBMCS')
build = t.build(repo.last_build_id)
build.restart()