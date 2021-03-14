from setuptools import setup, find_packages

setup(
    name='pychess',
    version='0.1.0',
    description='Some chess experiments',
    author='Lars Bergmann',
    author_email='lars@bergmann82.de',
    url='https://github.com/gandie',
    packages=find_packages(include=['pychess', 'pychess.*']),
    install_requires=[
        'chess',
    ],
    scripts=[
        'bin/lbchess-pieces',
        'bin/lbchess-randomgame',
    ],
    # package_data={'exampleproject': ['data/schema.json']}
)
