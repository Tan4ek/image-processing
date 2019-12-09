import unittest
from collections import namedtuple

from util.util import kafka_json_serializer, kafka_json_deserializer

_TestUser = namedtuple('TestUser', ['username', 'name', 'surname'])
_TestProxyUser = namedtuple('TestProxyUser', ['proxy_user', 'username'])


class TestUtil(unittest.TestCase):

    def test_kafka_json_serializer(self):
        payload = {
            'user': _TestUser('anonymous', 'Vasia', 'Pupkin'),
            'proxy_user': _TestProxyUser(_TestUser('client1', 'Boris', 'HrenUbiesh'), 'big_boss'),
            'array_user': [_TestUser('kek', 'Krutoi', 'Pomidor'), _TestUser('lol', 'Pokemon', 'Vsevolodovich')]
        }
        json_str = kafka_json_serializer(payload)
        restore_obj = kafka_json_deserializer(json_str)
        etalon_obj = {"user": {"username": "anonymous", "name": "Vasia", "surname": "Pupkin"},
                      "proxy_user": {"proxy_user": {"username": "client1", "name": "Boris", "surname": "HrenUbiesh"},
                                     "username": "big_boss"},
                      'array_user': [{'name': 'Krutoi', 'surname': 'Pomidor', 'username': 'kek'},
                                     {'name': 'Pokemon', 'surname': 'Vsevolodovich', 'username': 'lol'}]
                      }
        self.assertEqual(etalon_obj, restore_obj)

        payload_namedtuple = _TestUser('gorki', 'Maxim', 'Gorky')
        serialized_payload = kafka_json_serializer(payload_namedtuple)
        restore_payload_namedtuple = kafka_json_deserializer(serialized_payload)
        etalon_payload_namedtuple = {"username": "gorki", "name": "Maxim", "surname": "Gorky"}

        self.assertEqual(etalon_payload_namedtuple, restore_payload_namedtuple)
