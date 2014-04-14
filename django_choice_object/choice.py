import inspect
import operator
import six


class ChoiceMetaclass(type):
    def __init__(cls, name, type, other):
        # {value: (display_name, is_specified))
        cls._data = {}
        cls._order_key = 0 if (getattr(cls, "_order_by", "value") == "value") else 1

        for name, value in inspect.getmembers(cls):
            if not name.startswith("_") and \
                    not (inspect.isfunction(value) or inspect.ismethod(value)):
                if isinstance(value, tuple) and len(value) > 1:
                    value, display_name, is_specified = value[0], value[1], True
                else:
                    generated_name = " ".join([x.capitalize() for x in name.replace("_", " ").split(" ")])
                    value, display_name, is_specified = value, generated_name, False

                cls._data[value] = display_name
                setattr(cls, name, value)

        # So we need to access the ._data attribute of any parent classes so we can access the
        print(cls.__base__)

        if hasattr(cls.__base__, "_data"):
            data = cls.__base__._data
            # Go and patch up our values
            for value, name_data in data.items():
                cls._data[value] = name_data



        # Go through each of the classes bases and merge their ._data attribute, if it is a subclass of Choice
        # Only supports 1 level of inheritance ATM, with only a single parent (cant subclass 2 choice children).
        """for base_class in cls.__bases__:
            if not base_class == type[0] and issubclass(base_class, type):
                for index, data_item in enumerate(cls._data):
                    # Get the base classes values and update ours
                    base_class_item = filter(lambda i: i if i[0] == data_item[0] else None, base_class._data)
                    if len(base_class_item):
                        new_tuple = (data_item[0], base_class_item[0][1])
                        cls._data[index] = new_tuple"""

    def __iter__(self):
        for value, data in sorted(self._data.items(), key=lambda i: i[0] if self._order_key == 0 else i[1]):
            yield value, data


class ChoiceBase(object):
    _order_by = "value"

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


class Choice(six.with_metaclass(ChoiceMetaclass, ChoiceBase)):
    pass