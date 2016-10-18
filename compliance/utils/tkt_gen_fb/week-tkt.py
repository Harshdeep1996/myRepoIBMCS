from datetime import datetime, timedelta
from fb_ticket_mechanism import FogbugzTicketGenerator

week = 7 * 24 * 60
master_repo = 'evidence_weekly_master'
title_interval = 5 * 24 * 60
title_date = datetime.now() + timedelta(minutes=title_interval)


def make_init_case(title, parent_tkt, tag=None):
    return {
        'sTitle': '%s %d.%d.%d' % (title, title_date.day,
                                   title_date.month, title_date.year),
        'sTags': tag, 'ixBugParent': parent_tkt}


def test_parent_weekly_ticket():
    master_ticket = FogbugzTicketGenerator(
        master_repo, None,
        sTitle="Security and Compliance Weekly Master Ticket")
    master_ticket.setting_up()
    nessus(master_ticket.case_id)
    system_exported(master_ticket.case_id)
    remediate_apars(master_ticket.case_id)


def nessus(case_id):
    nessus_parent_tkt = FogbugzTicketGenerator(
        '{}/parent_nessus'.format(master_repo), None, **make_init_case(
            "Remediating Nessus Scan Parent Ticket", case_id))
    nessus_parent_tkt.setting_up()

    nessus_weekly = FogbugzTicketGenerator(
        '{}/evidence_nessus'.format(nessus_parent_tkt.repo_name),
        week, template_name='nessus_make_ticket_weekly.txt',
        **make_init_case(
            'Remediate Nessus Scan', nessus_parent_tkt.case_id, 'Nessus'))
    nessus_weekly.setting_up()


def system_exported(case_id):

    sys_exported_parent_tkt = FogbugzTicketGenerator(
        '{}/parent_sys_export'.format(master_repo), None, **make_init_case(
            "System Export Report Parent Ticket", case_id))
    sys_exported_parent_tkt.setting_up()

    system_exported_weekly = FogbugzTicketGenerator(
        '{}/evidence_sys_export_child'.format(
            sys_exported_parent_tkt.repo_name), week, **make_init_case(
            'System Export Report', sys_exported_parent_tkt.case_id, 'SOC2'))
    system_exported_weekly.setting_up()


def remediate_apars(case_id):

    rem_apars_parent_tkt = FogbugzTicketGenerator(
        '{}/parent_rem_apars'.format(master_repo), None, **make_init_case(
            "Remediate APARs Parent Ticket", case_id))
    rem_apars_parent_tkt.setting_up()

    rem_apars_weekly = FogbugzTicketGenerator(
        '{}/evidence_rem_apars_child'.format(rem_apars_parent_tkt.repo_name),
        week, **make_init_case('Remediate APARs', rem_apars_parent_tkt.case_id,
                               'SOC2'))
    rem_apars_weekly.setting_up()

if __name__ == '__main__':
    test_parent_weekly_ticket()
