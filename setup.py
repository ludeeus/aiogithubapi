"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()

setuptools.setup(
    name="aiogithubapi",
    version="0.3.0",
    author="Joakim Sorensen (@ludeeus)",
    author_email="hi@ludeeus.dev",
    description="Python async client for the GitHub API.",
    install_requires=["aiohttp", "async_timeout", "backoff"],
    long_description=LONG,
    long_description_content_type="text/markdown",
    url="https://github.com/ludeeus/aiogithubapi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
