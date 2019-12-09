import json
import socket
import time


class NamedtupleEncoder(json.JSONEncoder):

    @staticmethod
    def is_namedtuple(obj):
        return isinstance(obj, tuple) and hasattr(obj, '_asdict')

    @staticmethod
    def _replace_namedtuple_recursive_clone(obj):
        if isinstance(obj, dict):
            keys = list(obj.keys())
            clone_obj = {}
            for key in keys:
                value = obj[key]
                if NamedtupleEncoder.is_namedtuple(value):
                    value = value._asdict()
                value = NamedtupleEncoder._replace_namedtuple_recursive_clone(value)
                clone_obj[key] = value
            return clone_obj
        if isinstance(obj, list):
            clone_list = []
            for original_element in obj:
                clone_element = NamedtupleEncoder._replace_namedtuple_recursive_clone(original_element)
                clone_list.append(clone_element)
            return clone_list
        if NamedtupleEncoder.is_namedtuple(obj):
            return NamedtupleEncoder._replace_namedtuple_recursive_clone(obj._asdict())
        return obj

    def encode(self, obj):
        fixed_clone_obj = NamedtupleEncoder._replace_namedtuple_recursive_clone(obj)
        return super(NamedtupleEncoder, self).encode(fixed_clone_obj)


def kafka_json_serializer(v):
    return json.dumps(v, cls=NamedtupleEncoder).encode('utf-8')


def kafka_json_deserializer(v):
    return json.loads(v.decode('utf-8'))


def current_milli_time():
    return int(round(time.time() * 1000))


def get_hostname():
    return socket.gethostname()
