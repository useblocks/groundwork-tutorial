"""
csv-manager
===========
"""
from setuptools import setup, find_packages
import re
import ast

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('csv_manager/version.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='csv_manager',
    version=version,
    url='http://csv_manager.readthedocs.org',
    license='MIT license',
    author='team awesome',
    author_email='team_awesome@provider.com',
    description="Package for hosting groundwork apps and plugins like csv_manager_app or csv_manager_plugin.",
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
                            "csv_manager.applications.csv_manager_app:start_app"],
        'groundwork.plugin': ["csv_manager_plugin = "
                              "csv_manager.plugins.csv_manager_plugin:"
                              "csv_manager_plugin"],
    }
)
