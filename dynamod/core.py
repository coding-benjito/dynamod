from collections import namedtuple


class ConfigurationError(Exception):
    pass

DynamodDesc = namedtuple('DynamodDesc', ('basis', 'params', 'properties', 'progressions'), defaults=(None, None, None, None))
DynamoProp = namedtuple('DynamoProp', ('values', 'shares'))

