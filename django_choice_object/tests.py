import unittest
from .choice import Choice


class TestChoice(Choice):
    FIRST = 1, "zed"
    SECOND = 2
    THIRD = 3
    FOURTH = 4, "a description"
    WITH_UNDERSCORE = 5
    MORE_VALUES = 6, "another description"


class TestChoiceInheritance(TestChoice):
    EXTRA_VALUE = 7
    pass


class TestChoiceOrdered(TestChoice):
    ZED = 7, "zzzzzzzzz"
    _order_by = "name"


def get_name_from_choices(value, choices):
    for id, name in choices:
        if id == value:
            return name


class TestChoices(unittest.TestCase):
    def testInstance(self):
        i = TestChoice()
        self.failUnlessEqual(list(i), list(TestChoice))

    def testInheritance(self):
        self.failUnlessEqual(list(TestChoiceInheritance)[:-1], list(TestChoice))

    def testNames(self):
        fourth_name = get_name_from_choices(TestChoice.FOURTH, list(TestChoice))
        self.failUnlessEqual(fourth_name, "a description")

        underscore_name = get_name_from_choices(TestChoice.WITH_UNDERSCORE, list(TestChoice))
        self.failUnlessEqual(underscore_name, "With Underscore")

        self.failUnlessEqual(TestChoice.GetByName("a description"), TestChoice.FOURTH)
        self.failUnlessEqual(TestChoice.GetByValue(TestChoice.FOURTH), fourth_name)

    def testOrderBy(self):
        self.failIfEqual(list(TestChoice), list(TestChoiceOrdered))
        self.failUnless(list(TestChoiceOrdered)[-1][0] == TestChoiceOrdered.ZED)
        self.failUnlessEqual(list(TestChoice)[0][0], TestChoice.FIRST)




if __name__ == "__main__":
    unittest.main()
