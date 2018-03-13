from setuptools import setup, find_packages

setup(
    name='katsudon',
    version='0.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=[
        'click',
        'aiohttp',
        'asyncpg',
        'psycopg2',
        'sqlalchemy',
        'colorama',
        'cookiecutter',
        'pyaml'
    ],
    entry_points='''
        [console_scripts]
        katsudon=katsudon.cli:cli
    ''',
)
