from setuptools import setup
import os
from git_manager.db import db_directory

if not os.path.exists(db_directory):
    os.makedirs(db_directory)


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='gitmanager',
    description='A tool for managing multiple git projects.',
    long_description=read('README.rst'),
    version='0.1.1',
    packages=['git_manager'],
    install_requires=[
        'Click',
        'GitPython',
        'delegator.py',
        'sqlalchemy',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        gim=git_manager.cli:cli
    ''',
    classifiers=[
        'Topic :: Utilities',
        'Topic :: Software Development :: Version Control',
        'Topic :: Software Development :: Version Control :: Git'
    ]
)