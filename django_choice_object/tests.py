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


class TestCustomOrdering(Choice):
    LAST = ('last', 'Last', 10)
    FIRST = ('first', 'First', 1)

    @staticmethod
    def _get_sort_key(value):
        return value[2]


class TestCustomOrderingInheritance(TestCustomOrdering):
    MIDDLE = ('middle', 'Middle', 5)


class TestSimple(Choice):
    OTHER = 10


class TestMultipleInheritance(TestChoice, TestSimple):
    pass


def get_name_from_choices(value, choices):
    for id, name in choices:
        if id == value:
            return name


class TestChoices(unittest.TestCase):
    def testInstance(self):
        self.failUnlessEqual(list(TestChoice()), list(TestChoice))
        self.failUnlessEqual(list(TestChoiceOrdered()), list(TestChoiceOrdered))
        self.failUnlessEqual(list(TestChoiceInheritance()), list(TestChoiceInheritance))

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

    def testCustomOrdering(self):
        self.assertEqual(list(TestCustomOrdering)[0][0], TestCustomOrdering.FIRST)
        self.assertEqual(list(TestCustomOrdering)[-1][0], TestCustomOrdering.LAST)
        self.assertEqual(list(TestCustomOrderingInheritance)[0][0], TestCustomOrdering.FIRST)
        self.assertEqual(list(TestCustomOrderingInheritance)[-1][0], TestCustomOrdering.LAST)

    def testMultipleInheritance(self):
        self.assertEqual(list(TestMultipleInheritance), list(TestChoice) + list(TestSimple))


if __name__ == "__main__":
    unittest.main()
