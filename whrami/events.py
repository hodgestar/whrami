""" Whrami events. """

import json
import functools


class WhramiEvent:
    def __init__(self, etype, **kw):
        self._payload = {"etype": etype}
        self._payload.update(kw)

    def __getitem__(self, key):
        return self._payload[key]

    def __getattr__(self, key):
        return self._payload[key]

    @classmethod
    def from_json(cls, data):
        params = json.loads(data)
        etype = params.pop("etype")
        return cls(etype, **params)

    def to_json(self):
        return json.dumps(self._payload)


def parse_event(data):
    return WhramiEvent.from_json(data)


def close_web_socket():
    return WhramiEvent("close_web_socket")


def user_input(content):
    return WhramiEvent("user_input", content=content)


def user_output(content):
    return WhramiEvent("user_output", content=content)
