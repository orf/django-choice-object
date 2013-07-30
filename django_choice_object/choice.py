import inspect
import operator

class Choice(object):

    class __metaclass__(type):
        def __init__(cls, name, type, other):
            cls._data = []

            for name, value in inspect.getmembers(cls):
                if not name.startswith("_") and\
                        not (inspect.isfunction(value) or inspect.ismethod(value)):
                    if isinstance(value, tuple) and len(value) > 1:
                        data = value
                    else:
                        data = (value, " ".join([x.capitalize() for x in name.replace("_"," ").split(" ")]),)
                    cls._data.append(data)
                    setattr(cls, name, data[0])

            # Go through each of the classes bases and merge their ._data attribute, if it is a subclass of Choice
            # Only supports 1 level of inheritance ATM, with only a single parent (cant subclass 2 choice children).
            for base_class in cls.__bases__:
                if not base_class == type and issubclass(base_class, type):
                    for index, data_item in enumerate(cls._data):
                        # Get the base classes values and update ours
                        base_class_item = filter(lambda i: i if i[0] == data_item[0] else None, base_class._data)
                        if len(base_class_item):
                            new_tuple = (data_item[0], base_class_item[0][1])
                            cls._data[index] = new_tuple

        def __iter__(self):
            for value, data in sorted(self._data, key=operator.itemgetter(0)):
                yield value, data

    @classmethod
    def GetByValue(cls, value):
        return dict(cls)[value]

    @classmethod
    def GetByName(cls, name):
        if name is None:
            return None

        for value, data in cls._data:
            if name.lower() == data.lower():
                return value

        for dirname in dir(cls):
            if dirname.lower() == name.lower():
                return getattr(cls, dirname)

        return None