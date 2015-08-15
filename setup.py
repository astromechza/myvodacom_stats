from setuptools import setup

setup(
    # package info
    name='myvodacom_stats',
    version='0.1',
    description='A simple package for querying bundle balances for a myvodacom account',
    packages=['myvodacom_stats'],

    # runtime scripts
    scripts=['bin/vodacom-balances'],

    # requirements
    install_requires=['requests'],
)
