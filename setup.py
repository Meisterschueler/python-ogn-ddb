#!/usr/bin/env python3

from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ogn-ddb',
    version='0.0.1',
    description='The devices database for the Open Glider Network',
    long_description=long_description,
    url='https://github.com/Meisterschueler/python-ogn-ddb',
    author='Konstantin Gründger aka Meisterschueler',
    author_email='konstantin.gruendger@web.de',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='gliding ogn',
    packages=find_packages(exclude=['tests', 'tests.*']),
    python_requires='>=3',
    install_requires=[
        'Flask==1.1.2',
        'Flask-SQLAlchemy==2.4.1',
        'Flask-Migrate==2.5.3',
        'Flask-Admin==1.5.6',
        'Flask-Login==0.5.0',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-Mail==0.9.1',
        'Flask-Babel==1.0.0',
        'Flask-WTF==0.14.3',
        'email_validator==1.0.5',
        'WTForms-SQLAlchemy==0.1',
        'PyJWT==1.7.1',
    ],
    test_require=[
        'pytest==5.0.1',
        'flake8==1.1.1',
    ],
    extras_require={
	'heroku': ['gunicorn', 'psycopg2'],
    },
    zip_safe=False
)
