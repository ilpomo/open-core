from setuptools import setup, find_packages


def parse_requirements(filename: str) -> list[str]:

    with open(file=filename, mode='r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]


setup(
    name='open-core',
    version='0.1.0',
    author='Thomas Cercato',
    author_email='thomas.cercato@gmail.com',
    description='Event-based processing framework.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ilpomo/open-core',
    packages=find_packages(exclude=('asset', 'tests', 'tests.*')),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPL-3.0 License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires=parse_requirements(filename='requirements.txt'),
    extras_require={
        'dev': parse_requirements(filename='requirements-dev.txt'),
        'test': ['pytest', 'pytest-asyncio', 'pytest-mock', 'setuptools']
    },
)
