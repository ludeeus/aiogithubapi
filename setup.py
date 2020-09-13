"""Setup configuration."""
import setuptools
from aiogithubapi.common.const import VERSION

with open("README.md", "r") as fh:
    DESCRIPTION = fh.read()

setuptools.setup(
    name="aiogithubapi",
    version=VERSION,
    author="Joakim Sorensen (@ludeeus)",
    author_email="hi@ludeeus.dev",
    description="Asynchronous Python client for the GitHub API",
    install_requires=["aiohttp>=3.6.1,<4.0", "async_timeout", "backoff"],
    long_description=DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/aiogithubapi",
    packages=setuptools.find_packages(
        exclude=["tests", "tests.*", "generate", "generate.*"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
