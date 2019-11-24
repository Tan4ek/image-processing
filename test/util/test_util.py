import unittest
from collections import namedtuple

from util.util import kafka_json_serializer, kafka_json_deserializer

_TestUser = namedtuple('TestUser', ['username', 'name', 'surname'])
_TestProxyUser = namedtuple('TestProxyUser', ['proxy_user', 'username'])


class TestUtil(unittest.TestCase):

    def test_kafka_json_serializer(self):
        payload = {
            'user': _TestUser('anonymous', 'Vasia', 'Pupkin'),
            'proxy_user': _TestProxyUser(_TestUser('client1', 'Boris', 'HrenUbiesh'), 'big_boss')
        }
        json_str = kafka_json_serializer(payload)
        restore_obj = kafka_json_deserializer(json_str)
        etalon_obj = {"user": {"username": "anonymous", "name": "Vasia", "surname": "Pupkin"},
                      "proxy_user": {"proxy_user": {"username": "client1", "name": "Boris", "surname": "HrenUbiesh"},
                                     "username": "big_boss"}}
        self.assertEqual(etalon_obj, restore_obj)
