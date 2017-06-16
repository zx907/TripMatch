from setuptools import setup
setup(
    name='RMA',
    packages=['RMA'],
    include_package_data=True,
    install_requires=['flask', 'SQLAlchemy', 'pandas'],
)