"""
A setuptools based setup module.
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

description = 'datatoolkit for MLOps projects'

setup(
    name='datatoolkit',
    version='0.0.1',
    description=description,
    long_description=description,
    long_description_content_type='text/x-rst',
    url='a',
    author='Igor Malashchuk, CSC',
    author_email='a',
    license='CSC',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: MLOps Users',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='datatoolkit yaml_file MLOps',
    packages=find_packages(),
    install_requires=['jinja2>=2.7', 'pyyaml', 'prettytable', 'gitpython'],
    entry_points={
        'console_scripts': [
            'datatoolkit = datatoolkit.main:main'
        ]
    },
)
