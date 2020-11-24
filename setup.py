from os import getenv
from os import path
from os import chdir
from os import popen
import time
# To use a consistent encoding
from codecs import open
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
chdir(here)

# Get the long description from the pypi file
# Using UTF8 and single newlines
with open(path.join(here, 'pypi.md'), 'rb') as f:
    long_description = f.read().decode("utf-8").replace('\r\n', '\n')

# Set the package name:
name = 'pyedbglib'

"""
Package version :
The version number follows the format major.minor.patch.build
major, minor and patch are set manually according to semantic versioning 2.0.0: https://semver.org
build is an incrementing number set by a build server
in case of installing from source, build is set to 'dev' as allowed by PEP440
"""

# Package version setup
PACKAGE_VERSION = {
    "major": 2,  # Set the major version
    "minor": 16,  # Set the minor number
    "patch": 2,  # Set the patch number
    "build": 'dev0',  # Source distributions use "dev" as build number
}

version = "{}.{}.{}.{}".format(PACKAGE_VERSION['major'], PACKAGE_VERSION['minor'], PACKAGE_VERSION['patch'], PACKAGE_VERSION['build'])
print("Building {} version: {}".format(name, version))

# Create a "version.py" file in the package
fname = "{}/version.py".format(name)
with open(path.join(here, fname), 'w') as f:
    f.write("\"\"\" This file was generated when {} was built \"\"\"\n".format(name))
    f.write("VERSION = '{}'\n".format(version))
    # The command below can fail if git command not available, or not in a git workspace folder
    result = popen("git rev-parse HEAD").read()
    commit_id = result.splitlines()[0] if result else "N/A"
    f.write("COMMIT_ID = '{}'\n".format(commit_id))
    f.write("BUILD_DATE = '{}'\n".format(time.strftime("%Y-%m-%d %H:%M:%S %z")))
    f.close()

setup(
    name=name,
    version=version,
    description='Low-level protocol library for communicating with Microchip CMSIS-DAP based debuggers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='http://www.microchip.com',
    licence='Microchip Technology Inc. Proprietary License',
    author='Microchip Technology',
    author_email='support@microchip.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Embedded Systems',
        'License :: Other/Proprietary License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    packages=find_packages(exclude=['tests']),

    # List of packages required to use this package
    install_requires=[
        'cython<0.29.8;python_version<="2.7"', # To ensure there exists a wheel for win32/py27
        'cython;python_version>="3"', # No requirements going forward
        'hidapi',
        'pyserial'
    ],

    # List of packages required to develop and test this package
    #   $ pip install pyedbglib[dev]
    extras_require={
        'dev': ['pylint'],
    },

    # Include files from MANIFEST.in
    include_package_data=True,
)
