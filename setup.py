from setuptools import setup
import os
from git_manager.db import db_directory

if not os.path.exists(db_directory):
    os.makedirs(db_directory)

setup(
    name='gitmanager',
    version='0.1',
    py_modules=['git_manager'],
    install_requires=[
        'Click',
        'GitPython',
        'delegator',
        'sqlalchemy',
        'termcolor'
    ],
    entry_points='''
        [console_scripts]
        gim=git_manager.cli:cli
    ''',
)