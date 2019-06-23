import pytest
from protocol import make_response
from datetime import datetime

@pytest.fixture
def action_fixture():
    return 'echo'

@pytest.fixture
def time_fixture():
    return datetime.now().timestamp()

@pytest.fixture
def user_fixture():
    return 'some user'


@pytest.fixture
def request_fixture(action_fixture, time_fixture, user_fixture):
    return {
        'action': action_fixture,
        'time': time_fixture,
        'user': user_fixture,
    }

@pytest.fixture
def code_fixture():
    return 200

@pytest.fixture
def data_fixture():
    return 'some data'

@pytest.fixture
def response_fixture(action_fixture, user_fixture, time_fixture, data_fixture, code_fixture):
    return {
        'action': action_fixture,
        'user': user_fixture,
        'time':  time_fixture,
        'data': data_fixture,
        'code': code_fixture
    }

def test_make_response(request_fixture, code_fixture, data_fixture):
    response = make_response(request_fixture, code_fixture, data_fixture)

    assert response.get('action') == request_fixture.get('action')