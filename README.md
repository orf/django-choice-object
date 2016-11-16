Django choice object
====================

[![Build Status](https://travis-ci.org/orf/django-choice-object.svg?branch=master)](https://travis-ci.org/orf/django-choice-object)

I am a choice object for Django. I make using choices in forms and models easier.


### Usage

Choice classes inherit from Choice. Each attribute can have one or two values, the first being the value to be stored in the database and the second optional one being the display text. If no display text is given then it is created from the attribute name.

#### Example
```python
from django_choice_object import Choice
from django.db import models
    
class SomeChoice(Choice):
    FIRST_CHOICE = 1
    SECOND_CHOICE = 2
    THIRD_CHOICE = 3
    LAST_CHOICE = 4, "I am the display text"
    
class SomeModel(models.Model):
    some_field = models.IntegerField(choices=SomeChoice)
    
>>> list(SomeChoice)
[(1, 'First Choice'), (2, 'Second Choice'), (3, 'Third Choice'), (4, 'I am the display text')]
>>> SomeModel.objects.filter(some_field=SomeChoice.FIRST_CHOICE).all()
[object list...]
>>> SomeModel.objects.get(id=1).some_field
1
>>> SomeModel().some_field = SomeChoice.LAST_CHOICE
```

#### Advanced stuff

##### Grouping

Grouping choice values is a fairly common need. You can add groups of values to a choice like so:


```python
class ChoiceWitHGroups(Choice):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    
    START_GROUP = {FIRST, SECOND}
    END_GROUP = {THIRD, FOURTH}
```

Any value that ends with `_GROUP` and is a `set` will be ignored as a choice.


##### Ordering

Choices can be ordered in three ways. The default is by the value, but this can be configured using the 
`_order_by` attribute:

```python
class TestChoiceOrdered(Choice):
    LAST = 1, "zzzzzzzzz"
    FIRST = 2, "aaaaaaaa"
    _order_by = "name"
```

In the code snippet above the `FIRST` attribute would appear first as they are sorted by the 
name rather than the value.

You can also specify a custom sorting key:

```python
class WeirdChoice(Choice):
    LAST = 'last', 'Last', 10
    FIRST = 'first', 'First', 1

    @staticmethod
    def _get_sort_key(value):
        return value[2]
```

In this case the third item in the tuple would be the item to sort on.

### Contributing

- Set up a virtualenv: `virtualenv .`
- Install the requirements: `pip install -r requirements.txt`
- Run the tests: `nosetests .`
