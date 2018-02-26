from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.project_name}}',
    version='0.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=[
        "katsudon",
    ],
    entry_points='''
        [console_scripts]
        {{cookiecutter.package_name}}={{cookiecutter.package_name}}.cli:cli
    ''',
)

