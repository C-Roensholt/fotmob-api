from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requirements = f.readlines()

with open("README.md") as f:
    long_description = f.read()

setup(
    name="fotmob-api",
    version="0.0.1",
    description="API wrapper for Fotmob",
    author="Christian Rønsholt",
    author_email="ronsholt32@gmail.com",
    license="MIT",
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "test": ["pytest", "python-dotenv"],
        "examples": [
            "pandas>=2.2",
            "plottable>=0.1.5",
            "matplotlib>=3.8.2",
            "mplsoccer",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
)
