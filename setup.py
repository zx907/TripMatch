from setuptools import setup, find_packages
setup(
    name='TripMatch',
    version='0.1',
    description='A trip matching website for solo travelers',
    author='caveman2015',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['flask', 'sqlalchemy', 'flask-restful', 'wtforms'],
)