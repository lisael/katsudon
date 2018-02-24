from setuptools import setup

setup(
    name='katsudon',
    version='0.1',
    packages=['katsudon', 'katsudon.app', 'katsudon.apps', 'katsudon.apps.migrations', 'katsudon.conf', 'katsudon.db'],
    include_package_data=True,
    install_requires=[
        'click',
        'aiohttp',
        'asyncpg',
        'psycopg2',
        'sqlalchemy',
        'colorama',
        'pyyaml'
    ],
    entry_points='''
        [console_scripts]
        katsudon=katsudon.cli:cli
    ''',
)
