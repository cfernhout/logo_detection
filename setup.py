from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

setup(
    name="slug",
    version="0.0.0",
    packages=find_packages(include=['slug', 'slug/*']),
    install_requires=install_requires,
)
