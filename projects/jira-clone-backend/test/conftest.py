from __init__ import create_app
import pytest


@pytest.fixture(scope='module')
def test_client():
    with create_app().test_client() as client:
        yield client
