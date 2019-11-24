import json
import socket
import time


class NamedtupleEncoder(json.JSONEncoder):

    @staticmethod
    def is_namedtuple(obj):
        return isinstance(obj, tuple) and hasattr(obj, '_asdict')

    @staticmethod
    def _replace_namedtuple_recursive_clone(obj_dict):
        keys = list(obj_dict.keys())
        clone_obj = {}
        for key in keys:
            value = obj_dict[key]
            if NamedtupleEncoder.is_namedtuple(value):
                value = value._asdict()
            if isinstance(value, dict):
                value = NamedtupleEncoder._replace_namedtuple_recursive_clone(value)
            clone_obj[key] = value
        return clone_obj

    def encode(self, obj):
        if isinstance(obj, dict):
            fixed_clone_obj = NamedtupleEncoder._replace_namedtuple_recursive_clone(obj)
            return super(NamedtupleEncoder, self).encode(fixed_clone_obj)

        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            return super().encode(obj._asdict())
        return super(NamedtupleEncoder, self).encode(obj)


def kafka_json_serializer(v):
    return json.dumps(v, cls=NamedtupleEncoder).encode('utf-8')


def kafka_json_deserializer(v):
    return json.loads(v.decode('utf-8'))


def current_milli_time():
    return int(round(time.time() * 1000))


def get_hostname():
    return socket.gethostname()
