import os
import codecs
import re

from setuptools import setup, find_packages
import webapi

here = os.path.abspath(os.path.dirname(__file__))
README = ''
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

requires = [
    'celery==4.1.0',
    'pymongo==3.6.0',
    'mongoengine==0.15.0',
    'jsonschema==2.6.0',
    'falcon==1.4.1',
    'PyJWT==1.6.0',
    'falcon-auth==1.1.0',
    'falcon-cors==1.1.7',
    'gevent==1.2.2'
]

tests_require = [
    'mongoengine==0.15.0',
    'mongomock==3.9.0',
    'falcon==1.4.1',
    'PyJWT==1.6.0',
    'falcon-auth==1.1.0'
]

setup(
    name='webapi',
    version=find_version('webapi/version.py'),
    description='webapi',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Falcon',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='',
    author_email='',
    url='',
    keywords='web falcon',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    test_suite='tests'
)
