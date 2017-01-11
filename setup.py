"""
groundwork-tutorial
===================
"""
from setuptools import setup, find_packages
import re
import ast

setup(
    name='csv_manager',
    version="0.0.1",
    url='http://groundwork_tutorial.readthedocs.org',
    license='MIT license',
    author='team useblocks',
    author_email='info@useblocks.com',
    description="Reading and managing csv file readers",
    long_description=__doc__,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    platforms='any',
    setup_requires=[],
    tests_require=[],
    install_requires=['groundwork', 'pytest-runner', 'sphinx', 'gitpython'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': ["csv_manager = "
                            "csv_manager.applications.csv_manager:start_app"],
        'groundwork.plugin': ["csv_manager_plugin = "
                              "csv_manager.plugins.csv_reader:"
                              "csv_reader"],
    }
)
