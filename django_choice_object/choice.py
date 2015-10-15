import inspect
import six


class ChoiceMetaclass(type):
    def __init__(cls, name, typeof, other):
        cls._data = {}
        cls._order_key = 0 if (getattr(cls, "_order_by", "value") == "value") else 1

        for name, value in inspect.getmembers(cls):
            if not name.startswith("_") and \
                    not (inspect.isfunction(value) or inspect.ismethod(value) or type(value) is classmethod):
                if isinstance(value, tuple) and len(value) > 1:
                    value, display_name = value[0], value[1]
                    setattr(cls, name, value)
                else:
                    display_name = " ".join(x.capitalize() for x in name.split("_"))

                cls._data[value] = display_name

        # So we need to access the ._data attribute of any parent classes so we can access the
        if hasattr(cls.__base__, "_data"):
            data = cls.__base__._data
            # Go and patch up our values
            for value, name_data in data.items():
                cls._data[value] = name_data

    def __iter__(self):
        for value, data in sorted(self._data.items(), key=lambda i: i[0] if self._order_key == 0 else i[1]):
            yield value, data


class ChoiceBase(object):
    pass


class Choice(six.with_metaclass(ChoiceMetaclass, ChoiceBase)):
    _order_by = "value"

    def __iter__(self):
        for value, data in sorted(self._data.items(), key=lambda i: i[0] if self._order_key == 0 else i[1]):
            yield value, data

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
