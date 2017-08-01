#!/usr/bin/python3

import os
from setuptools import setup, find_packages


def get_requirements():
    requirements_txt = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'requirements.txt')
    with open(requirements_txt) as fd:
        lines = fd.read().splitlines()

    return list(line for line in lines if not line.startswith('#'))

setup(
    name='fabric8_analytics_firehose_fetcher',
    version='0.1',
    packages=find_packages(),
    install_requires=get_requirements(),
    py_modules='fetcher_cli',
    scripts=['fetcher_cli.py'],
    entry_points='''
        [console_scripts]
        cli=fetcher_cli:cli
    ''',
    include_package_data=True,
    author='Pavel Kajaba',
    author_email='pavel@redhat.com',
    description='fabric8-analytics libraries.io Firehose fetcher',
    license='ASL 2.0',
    keywords='fabric8 analytics firehose libraries.io',
    url='https://github.com/fabric8-analytics/fabric8-analytics-firehose-fetcher',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Intended Audience :: Developers",
    ]
)
