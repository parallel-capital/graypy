#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest
from graypy import GELFTCPHandler, GELFUDPHandler
from tests.helper import logger, get_unique_message, log_warning, TEST_KEY, \
    TEST_CERT


@pytest.fixture(params=[
    GELFTCPHandler(host='127.0.0.1', port=12201, debugging_fields=True),
    GELFTCPHandler(host='127.0.0.1', port=12201, tls=True,
                   tls_client_cert=TEST_CERT,
                   tls_client_key=TEST_KEY,
                   tls_client_password="secret"),
    GELFUDPHandler(host='127.0.0.1', port=12202, debugging_fields=True),
    GELFUDPHandler(host='127.0.0.1', port=12202, debugging_fields=True, compress=False),
])
def handler(request):
    return request.param


def test_debug_mode(logger):
    message = get_unique_message()
    graylog_response = log_warning(logger, message)
    assert graylog_response['message'] == message
    assert graylog_response['file'] == 'helper.py'
    assert graylog_response['module'] == 'helper'
    assert graylog_response['func'] == 'log_warning'
    assert graylog_response['logger_name'] == 'test'
    assert 'line' in graylog_response
