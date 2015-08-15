from setuptools import setup

setup(
    # package info
    name='myvodacom_stats',
    version='0.1',
    description='',
    packages=['myvodacom_stats'],

    # runtime scripts
    scripts=['bin/vodacom-balances'],

    # requirements
    install_requires=['requests'],
)
