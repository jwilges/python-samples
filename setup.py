import codecs
import importlib
import re
import subprocess
import sys
from pathlib import Path

import distutils
import setuptools
import setuptools.command.build_py


def read(source_file_name: Path):
    if not source_file_name.is_file():
        raise FileNotFoundError(source_file_name)
    with codecs.open(source_file_name, 'r') as source_file:
        return source_file.read()


HERE = Path().parent.absolute()
PACKAGE_PATH = HERE / 'samples'

LONG_DESCRIPTION = read(HERE / 'README.md')
METADATA = {
    'name': 'samples',
    'version': '0.0.0',
    'author': 'Jeffrey Wilges',
    'author_email': 'jeffrey@wilges.com',
    'description': 'python samples',
    'url': 'https://github.com/jwilges/python-samples',
    'license': 'BSD'
}


setuptools.setup(
    **METADATA,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['tests*']),
    python_requires='>=3.6',
    install_requires=[
        'dataclasses; python_version < "3.7"'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: Console',
        'Topic :: Utilities'
    ],
)
