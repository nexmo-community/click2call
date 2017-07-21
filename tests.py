import json
import pytest
from urllib.parse import urlencode
from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application
from app import NexmoConfig, NCCOHandler, MainHandler

CONFIG_TEST_VALUES = [
    ('MY_NUMBER', '44771234567'),
    ('MY_LVN', '44123456789'),
    ('APP_ID', 'CLICK2CALL_TEST'),
    ('URL', 'https://example.com'),
    ('PRIVATE_KEY', 'DUMMY_KEY_VALUE'),
]


class TestNexmoConfig(object):

    def setup_class(self):
        self.config = NexmoConfig()

    @pytest.mark.parametrize('key,expected_value', CONFIG_TEST_VALUES)
    def test_config_contains(self, key, expected_value):
        assert hasattr(self.config, key)
        assert getattr(self.config, key) == expected_value


class TestNCCOHandler(AsyncHTTPTestCase):

    NAME = 'John Doe'
    NUMBER = '0123456789'
    RESPONSE = None

    def setup_class(self):
        self.NCCO_URL = '/?{qs}'.format(qs=urlencode({
            'name': self.NAME,
            'number': self.NUMBER
        }))

    def get_app(self):
        return Application([(r"/", NCCOHandler)])

    def _get_response(self):
        if not self.RESPONSE:
            self.http_client.fetch(
                self.get_url(self.NCCO_URL),
                self.stop,
                method="GET"
            )
            self.RESPONSE = self.wait()

        return self.RESPONSE

    def test_content_type(self):
        assert self._get_response().headers.get('Content-Type') == 'application/json'

    def test_ncco_has_two_actions(self):
        assert len(json.loads(self._get_response().body)) == 2

    def test_ncco_contains_number(self):
        assert json.loads(self._get_response().body)[1]['endpoint'][0]['number'] == self.NUMBER

    def test_ncco_contains_name(self):
        assert self.NAME in json.loads(self._get_response().body)[0]['text']


class TestMainHandler(AsyncHTTPTestCase):

    RESPONSE = None

    def get_app(self):
        return Application([(r"/", MainHandler)])

    def _get_response(self):
        if not self.RESPONSE:
            self.http_client.fetch(
                self.get_url('/'),
                self.stop,
                method="GET"
            )
            self.RESPONSE = self.wait()

        return self.RESPONSE

    def test_content_type(self):
        assert self._get_response().headers.get('Content-Type') == 'text/html'
