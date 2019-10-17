import pytest
import requests
import requests_mock

from mocker_client import MockServer, Mock, MockDupError


@pytest.fixture
def req_mock():
    with requests_mock.Mocker() as m:
        yield m


def test_create_mock(req_mock):
    req_mock.register_uri('POST', 'http://127.0.0.1:8080/mocker_api/mocks/',
                          json={'url': 'http://localhost:8080/mocker_api/mocks/1/', 'name': 'hi'})

    mock = MockServer().create_mock({'name': 'hi', 'route': '/q', 'method': 'get', 'responses': 'Hi_1'})
    assert mock.data['url'] == 'http://localhost:8080/mocker_api/mocks/1/'


def test_create_mocks(req_mock):
    req_mock.register_uri(
        'POST',
        'http://127.0.0.1:8080/mocker_api/mocks/',
        json=[
            {'url': 'http://localhost:8080/mocker_api/mocks/1/', 'name': 'hi'},
            {'url': 'http://localhost:8080/mocker_api/mocks/2/', 'name': 'ho'},
        ]
    )

    mocks = MockServer().create_mocks([
        {'name': 'hi', 'route': '/q', 'method': 'get', 'responses': 'Hi_1'},
        {'name': 'ho', 'route': '/w', 'method': 'get', 'responses': 'Hi_2'},
    ])
    assert len(mocks) == 2
    assert mocks[0].data['url'] == 'http://localhost:8080/mocker_api/mocks/1/'
    assert mocks[1].data['url'] == 'http://localhost:8080/mocker_api/mocks/2/'


def test_create_dup_mock(req_mock):
    req_mock.register_uri('POST', 'http://127.0.0.1:8080/mocker_api/mocks/',
                          json={'Failed': 'overlapped'}, status_code=409)

    with pytest.raises(MockDupError):
        MockServer().create_mock({'name': 'hi', 'route': '/q', 'method': 'get', 'responses': 'Hi_1'})


def test_create_dup_mocks(req_mock):
    req_mock.register_uri('POST', 'http://127.0.0.1:8080/mocker_api/mocks/',
                          json={'Failed': 'overlapped'}, status_code=409)

    with pytest.raises(MockDupError):
        MockServer().create_mocks([
            {'name': 'hi', 'route': '/q', 'method': 'get', 'responses': 'Hi_1'},
            {'name': 'ho', 'route': '/w', 'method': 'get', 'responses': 'Hi_2'},
        ])


def test_create_invalid_mock(req_mock):
    req_mock.register_uri('POST', 'http://127.0.0.1:8080/mocker_api/mocks/',
                          json={'Bad request': 'route is required'}, status_code=400)

    with pytest.raises(requests.exceptions.RequestException):
        MockServer().create_mock({'name': 'hi', 'method': 'get', 'responses': 'Hi_1'})


def test_create_invalid_mocks(req_mock):
    req_mock.register_uri('POST', 'http://127.0.0.1:8080/mocker_api/mocks/',
                          json={'Bad request': 'route is required'}, status_code=400)

    with pytest.raises(requests.exceptions.RequestException):
        MockServer().create_mocks([
            {'name': 'hi', 'method': 'get', 'responses': 'Hi_1'},
            {'name': 'ho', 'method': 'get', 'responses': 'Hi_2'},
        ])


def test_delete_mock(req_mock):
    req_mock.register_uri('DELETE', 'http://127.0.0.1:8080/mocker_api/mocks/1/',
                          json={'is_expired': False})

    mock = Mock({'url': 'http://127.0.0.1:8080/mocker_api/mocks/1/', 'name': 'test'})
    assert mock.delete()['is_expired'] is False
