from ado.version import ADO_VERSION
from setuptools import setup, find_packages

setup(
        name='ado',
        author='Ana Nelson',
        packages=find_packages(),
        version=ADO_VERSION,
        install_requires = [
            'python-modargs>=1.6'
            ],
        entry_points = {
            'console_scripts' : [ 'ado = ado.commands:run' ]
            }
        )

