from setuptools import setup
setup(
    name='TripMatch',
    packages=['TripMatch'],
    include_package_data=True,
    install_requires=['flask', 'SQLAlchemy'],
)