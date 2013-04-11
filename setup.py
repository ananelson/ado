from ado.version import ADO_VERSION
from setuptools import setup, find_packages

setup(
        name='ado',
        author='Ana Nelson',
        packages=find_packages(),
        version=ADO_VERSION,
        include_package_data = True,
        install_requires = [
            'python-modargs>=1.7',
            'Markdown', # for reports
            'dexy>=0.9.9'
            ],
        entry_points = {
            'console_scripts' : [ 'ado = ado.commands:run' ]
            }
        )

