import inspect
import six
import warnings

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class ChoiceMetaclass(type):
    def __init__(cls, cls_name, bases, attrs):
        cls._raw = []
        for base in bases:
            if hasattr(base, '_raw'):
                cls._raw += base._raw

        for name, value in attrs.items():
            if name.startswith("_"):
                continue
            if inspect.isfunction(value) or inspect.ismethod(value) or type(value) is classmethod:
                continue
            if name.endswith('_GROUP') and isinstance(value, set):
                continue

            if isinstance(value, tuple) and len(value) > 1:
                setattr(cls, name, value[0])
            else:
                display_name = " ".join(x.capitalize() for x in name.split("_"))
                value = (value, display_name)

            cls._raw.append(value)

        cls._raw = sorted(cls._raw, key=lambda item: cls._get_sort_key(item))

        cls._data = OrderedDict()
        for value in cls._raw:
            cls._data[value[0]] = value[1]

    def _iter(cls):
        warnings.warn(
            '_iter is deprecated, use __iter__ (via list()/iter()) instead'
        )
        return cls.__iter__(cls)

    def _get_sort_key(cls, value):
        _order_key = 0 if (getattr(cls, "_order_by", "value") == "value") else 1
        return value[_order_key]

    def __iter__(cls):
        for value, data in six.iteritems(cls._data):
            yield value, data


class ChoiceBase(object):
    pass


class Choice(six.with_metaclass(ChoiceMetaclass, ChoiceBase)):
    _order_by = "value"

    def __iter__(self):
        return iter(self.__class__)

    @classmethod
    def get_by_value(cls, value):
        return dict(cls)[value]

    @classmethod
    def get_by_name(cls, name):
        if name is None:
            return None

        for value, data in cls._data.items():
            if name.lower() == data.lower():
                return value

        for dirname in dir(cls):
            if dirname.lower() == name.lower():
                return getattr(cls, dirname)

        return None

    @classmethod
    def GetByValue(cls, value):
        warnings.warn(
            'GetByValue is deprecated, use get_by_value instead'
        )
        return cls.get_by_value(value)

    @classmethod
    def GetByName(cls, name):
        warnings.warn(
            'GetByName is deprecated, use get_by_name instead'
        )
        return cls.get_by_name(name)
