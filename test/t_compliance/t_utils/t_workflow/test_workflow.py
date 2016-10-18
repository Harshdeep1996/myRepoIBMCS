
# -*- coding:utf-8 -*-

import os
import shutil
import tempfile
from nose import with_setup
from nose.tools import assert_equals

from mock import patch, Mock, MagicMock, mock_open

from compliance.utils.fetch import fetch
from compliance.utils.evidence import Locker, Evidence
from compliance.utils.workflow import Workflow, FogbugzCaseWorkflow


e = Evidence(
    name='logo.svg',
    url='https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg',
    ttl=2592000,
    description='IBM Logo'
)


def test_set_evidence():
    '''
    Test adding evidence to the workflow
    '''
    workflow = Workflow(Locker())
    workflow.required_evidence([e])
    assert_equals(workflow.evidence, [e])


@patch('compliance.utils.evidence.Locker')
def test_validate_and_fetch(MockerLocker):
    '''
    Test that evidence it validated
    '''
    locker = MockerLocker()
    workflow = Workflow(locker)
    workflow.required_evidence([e])
    workflow.validate_and_fetch()
    test_for_passes = workflow.passes(report=True)
    assert_equals(test_for_passes, True)
    locker.validate.assert_called_with(e)


def copy_to_temp():
    dir_tuple = os.path.split(os.path.abspath(__file__))
    shutil.copy(dir_tuple[0] + '/demo_case.xml', tempfile.gettempdir())


def remove_from_temp():
    os.remove(tempfile.gettempdir() + "/" + "demo_case.xml")


@patch('compliance.utils.evidence.Locker')
@patch('os.path.exists')
def test_fb_workflow_with_case(MockerLocker, pathexists):
    copy_to_temp()
    locker = MockerLocker()
    pathexists.return_value = True
    locker.get_file.return_value = tempfile.gettempdir() + "/" + "demo_case.xml"
    workflow = FogbugzCaseWorkflow(locker, interval=10 * 365 * 24 * 60)
    workflow.closed = True
    test_for_passes = workflow.passes(report=True)
    assert_equals(test_for_passes, True)
    remove_from_temp()


@patch('compliance.utils.evidence.Locker')
@patch('os.path.exists')
@patch('compliance.utils.workflow.FogbugzCaseWorkflow._write_xml')
def test_fb_workflow_without_case(MockerLocker, pathexists, writexml):
    copy_to_temp()
    locker = MockerLocker()
    pathexists.return_value = False
    locker.get_file.return_value = tempfile.gettempdir() + "/" + "demo_case.xml"
    workflow = FogbugzCaseWorkflow(
        locker, init_case={}, interval=10 * 365 * 24 * 60)
    assert_equals(workflow.id, 75714)
    remove_from_temp()
