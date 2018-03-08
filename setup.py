from setuptools import setup
setup(
    name='TripMatch',
    version='0.1',
    description='A flask website',
    author='caveman2015',
    packages=['tripmatch'],
    include_package_data=True,
    install_requires=['flask', 'SQLAlchemy', 'werkzeug'],
)