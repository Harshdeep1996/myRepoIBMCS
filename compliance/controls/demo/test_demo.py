import requests
from nose import with_setup


def setup_func():
    "set up test fixtures"


def teardown_func():
    "tear down test fixtures"


@with_setup(setup_func, teardown_func)
def test_passes():
    r = requests.get('http://httpbin.org/status/200')
    assert r.status_code == 200


@with_setup(setup_func, teardown_func)
def test_fails():
    r = requests.get('http://httpbin.org/status/404')
    assert r.status_code == 200
