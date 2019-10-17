===========================
client for http mock server
===========================

.. image:: https://badge.fury.io/py/mocker-client.svg
    :target: https://badge.fury.io/py/mocker-client

.. image:: https://codecov.io/gh/vilus/mocker_client/branch/master/graph/badge.svg
     :target: https://codecov.io/gh/vilus/mocker_client

.. image:: https://travis-ci.org/vilus/mocker_client.svg?branch=master
       :target: https://travis-ci.org/vilus/mocker_client

python client for create/delete mocks on mock server


Example
--------
.. code-block:: bash

    pip install mocker-client


.. code-block:: python

    from mocker_client import MockServer, Mock


    mock = MockServer(url='http://127.0.0.1:8080/mocker_api/mocks/').create_mock(
        {'name': 'hi', 'route': '/q', 'method': 'get', 'responses': 'Hi_1'}
    )
    # actions
    mock.delete()
    #
    help(MockServer.create_mock)
    create_mock(self, data)
        :param data: dict with keys:
          'name' - optional, '' by default
          'route' - for example '/some_path'
          'method' - a http method like GET, POST, PUT, etc
          'response_type' - optional, choice from ['single', 'sequence', 'cycle'], 'single' by default
          'responses' - list of dicts with keys (or just dict if response_type is single):
            'body' - response body
            'return_code' - http status code, like 200
            'headers' - dict with http headers
        :returns Mock object
    #
    help(MockServer.create_mocks)
    create_mocks(self, list_data)
        :param list_data: list of dicts with keys:
          'name' - optional, '' by default
          'route' - for example '/some_path'
          'method' - a http method like GET, POST, PUT, etc
          'response_type' - optional, choice from ['single', 'sequence', 'cycle'], 'single' by default
          'responses' - list of dicts with keys (or just dict if response_type is single):
            'body' - response body
            'return_code' - http status code, like 200
            'headers' - dict with http headers
        :returns list of Mock objects
    #
    help(Mock.delete)
    delete(self)
        delete mock on server and return its info - {is_expired: bool}

