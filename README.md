Django choice object
====================

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
