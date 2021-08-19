from setuptools import find_packages, setup

VERSION = '0.0.2'

setup(
    name='basic_instagram_library',
    version=VERSION,
    author='Holden Karau',
    author_email='holden@pigscanfly.ca',
    packages=find_packages(),
    url='https://github.com/holdenk/distributedcomputing4kids/code/basic_instagram_library',
    license='LICENSE',
    description='A library to read an instagram users tags, a thin wrapper around instagram-scraper',
    long_description=open('README.md').read(),
    install_requires=[
        'instagram-scraper==1.10.2',
        'retry'
    ],
    test_requires=[
        'nose==1.3.7',
        'unittest2>=1.0.0',
    ],
)
