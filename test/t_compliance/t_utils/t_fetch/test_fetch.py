# -*- coding:utf-8 -*-

import os
import tempfile
from nose import with_setup
from nose.tools import assert_equals
from compliance.utils.fetch import fetch
from compliance.utils.evidence import Evidence


LOGO_PATH = os.path.join(tempfile.gettempdir(), 'logo.svg')


def clean_tmp():
    os.remove(LOGO_PATH)


@with_setup(teardown=clean_tmp)
def test_fetch():
    '''
    Test basic fetch from public site
    '''
    e = Evidence(
        name='logo.svg',
        url='https://upload.wikimedia.org/wikipedia/commons/5/51/IBM_logo.svg',
        ttl=2592000,
        description='IBM Logo'
    )

    assert_equals(fetch(e), LOGO_PATH)
