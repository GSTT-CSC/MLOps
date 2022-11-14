import setuptools

# from mlops import __version__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.8.0"

install_requires = ['mlflow==1.26.0'
                    'boto3',
                    'docker~=5.0.3',
                    'minio>=7.0.3',
                    'pytest>= 6.2',
                    'colorlog~=6.6.0',
                    'fsspec',
                    'monai',
                    'itk',
                    'tqdm',
                    'pandas',
                    'matplotlib',
                    'xnat',
                    'GitPython',
                    'protobuf~=3.19.0',
                    'PyYAML~=6.0',
                    'requests~=2.27.1',
                    'click~=8.1.2',
                    'setuptools~=57.0.0',
                    'torch']

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
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'mlops = mlops.cli:cli',
        ],
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
