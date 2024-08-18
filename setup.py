import os

from setuptools import setup, find_packages


def parse_requirements(filename: str) -> list[str]:

    filedir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(filedir, filename)

    with open(file=filepath, mode='r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


setup(
    name='open-core',
    version='0.1.3',
    author='Thomas Cercato',
    author_email='thomas.cercato@gmail.com',
    description='Event-based processing framework.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ilpomo/open-core',
    packages=find_packages(
        exclude=('asset', 'example', 'tests',)),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL-3.0 License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=['msgspec~=0.18.6', 'pyzmq~=26.1.0', 'uvloop~=0.20.0'],
    extras_require={
        'dev': ['pytest~=8.3.2', 'pytest-asyncio~=0.23.8', 'pytest-mock~=3.14.0', 'setuptools~=72.2.0'],
    },
)