import setuptools
# from mlops import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.6.2"

setuptools.setup(
    name="csc-mlops",
    version=version,
    author="Laurence Jackson",
    author_email="laurence.jackson@gstt.nhs.uk",
    description="An MLOps framework for development of clinical applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GSTT-CSC/MLOps",
    project_urls={
        "Bug Tracker": "https://github.com/GSTT-CSC/MLOps/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
