import os
from utilitarian.credentials import Config
from compliance.utils.evidence import Locker
from jinja2 import Environment, FileSystemLoader
from compliance.utils.workflow import FogbugzCaseWorkflow
from utilitarian.services.tickets import connect_to_fogbugz

default_params_dict = {
    'sArea': 'Misc',
    'sProject': 'Security and Compliance',
    'sFixFor': 'Product Backlog',
    'ixPersonAssignedTo': 40,
    'ixPriority': '3',
    'plugin_customfields_at_fogcreek_com_squadi720': "Security and Compliance"}

creds = Config(os.path.expanduser('~/.credentials'))


class FogbugzTicketGenerator(object):

    def __init__(self, repo_name, interval, template_name=None, **kwargs):
        '''
        Initializes the repo name, and updates the parameters

        for the fogbugz ticket using the default and the one's set

        by the admin.
        '''
        self.repo_name = repo_name
        self.params_dict = kwargs.copy()
        self.params_dict.update(default_params_dict)
        if template_name is not None:
            get_template_render(template_name)
        self._fb = connect_to_fogbugz(creds=creds)
        self.interval = interval
        self.case_id = 0

    def setting_up(self):
        with Locker(self.repo_name) as locker:
            case = FogbugzCaseWorkflow(
                locker, init_case=self.params_dict, interval=self.interval)
            self.case_id = case.id
            case.validate_and_fetch()
            case.closed = True
            assert case.passes()

    def get_template_render(self, template_name):
        env = Environment(loader=FileSystemLoader('./templates'))
        result = env.get_template(template_name).render()
        default_params_dict['sEvent'] = result.decode('utf-8')
