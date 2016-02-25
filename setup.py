from setuptools import setup, find_packages
from codecs import open
import os


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='PyZureML',
    version='1.0.5',

    description='Python wrapper for the Microsoft Azure Machine Learning webservice endpoint API.',
    long_description=long_description,

    url='https://github.com/marcardioid/PyZureML',

    author='Marc Sleegers',
    author_email='mail@marcsleegers.com',

    license='MIT',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='microsoft azure machine learning webservice endpoint api wrapper',

    packages=find_packages(exclude=['docs', 'tests']),

    install_requires=['requests'],
)
