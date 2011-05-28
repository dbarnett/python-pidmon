import os
import sys
from setuptools import setup, find_packages

setup(
    name = "pidmon",
    version = "0.01",
    packages=find_packages(),
    dependency_links = [],
    install_requires=(['win32com'] if os.name == 'nt' else []),
    extras_require={},
    package_data = {},
    author="David Barnett",
    author_email = "davidbarnett2@gmail.com",
    description = "collection of hacks to monitor running processes",
    license = "BSD",
    keywords= "",
    test_suite='nose.collector',
    tests_require=['nose'],
    url = "http://github.com/dbarnett/python-pidmon",
    entry_points = {
        "console_scripts": [
            "pidmon = pidmon.__main__"
        ]
    }
)
