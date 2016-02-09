import inspect
import six

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

    def _iter(self):
        for value, data in six.iteritems(self._data):
            yield value, data

    def _get_sort_key(self, value):
        _order_key = 0 if (getattr(self, "_order_by", "value") == "value") else 1
        return value[_order_key]

    def __iter__(self):
        return self._iter()


class ChoiceBase(object):
    pass


class Choice(six.with_metaclass(ChoiceMetaclass, ChoiceBase)):
    _order_by = "value"

    def __iter__(self):
        return self.__class__._iter()

    @classmethod
    def GetByValue(cls, value):
        return dict(cls)[value]

    @classmethod
    def GetByName(cls, name):
        if name is None:
            return None

        for value, data in cls._data.items():
            if name.lower() == data.lower():
                return value

        for dirname in dir(cls):
            if dirname.lower() == name.lower():
                return getattr(cls, dirname)

        return None
