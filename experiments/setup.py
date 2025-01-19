from setuptools import setup,find_packages

setup(
    name="knsp",
    packages=find_packages(exclude=['docs', 'tests*', 'problems']),
    entry_points = {
        'console_scripts': [
            'knsp = knsp_cli.solver:main'
        ],
    }
)
