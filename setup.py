#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Paul Gierz",
    author_email='pgierz@awi.de',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Bootstrap esm-tools into a virtual environment to keep every experiment seperate",
    entry_points={
        'console_scripts': [
            'venv_bootstrap=venv_bootstrap.cli:main',
        ],
        "esm_tools.plugins": ["venv_bootstrap=venv_bootstrap.venv_bootstrap:venv_bootstrap"],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='venv_bootstrap',
    name='venv_bootstrap',
    packages=find_packages(include=['venv_bootstrap']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/pgierz/venv_bootstrap',
    version='0.1.0',
    zip_safe=False,
)
