from travispy import TravisPy
from utilitarian.credentials import Config

creds = Config(os.path.expanduser('~/.credentials'))

t = TravisPy.github_auth(creds['github'].token)

repo = t.repo('clouddataservices/cloudant-compliance-checks')
build = t.build(repo.last_build_id)
build.restart()
