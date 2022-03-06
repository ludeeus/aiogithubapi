"""Setup configuration."""
from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Ludeeus",
    author_email="hi@ludeeus.dev",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Asynchronous Python client for the GitHub API",
    install_requires=["aiohttp>=3.6.1,<4.0", "async_timeout", "backoff>=1.10.0", "pydantic>=1.9.0"],
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=readme,
    python_requires=">=3.8",
    name="aiogithubapi",
    packages=find_packages(include=["aiogithubapi", "aiogithubapi.*"]),
    version="main",
    url="https://github.com/ludeeus/aiogithubapi",
)
