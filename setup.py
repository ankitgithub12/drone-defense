from setuptools import setup, find_packages

setup(
    name="drone-defense",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        'flask>=2.3.2',
        'gunicorn>=20.1.0',
        'numpy>=1.24.3'
    ],
    python_requires='>=3.9',
)