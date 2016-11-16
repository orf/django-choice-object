from setuptools import setup
import sys

install_requires = ["six"]

if sys.version_info < (2, 7):
    install_requires.append("ordereddict")

setup(
    name='django-choice-object',
    version='0.8',
    packages=['django_choice_object'],
    url='https://github.com/orf/django-choice-object',
    license='',
    author='Tom',
    author_email='tom@tomforb.es',
    description='A choice object for Django forms and models',
    install_requires=install_requires
)
