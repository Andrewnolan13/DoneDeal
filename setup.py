#setup.py
from setuptools import setup, find_packages

setup(
    name='donedeal',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'numpy',
        'plotly',
        'datetime'],
    entry_points={
        'console_scripts': [
            'donedeal = donedeal.__main__:main'
        ]
    }
)
