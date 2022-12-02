import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = "0.9.15"

install_requires = [
    'mlflow==2.0.1',
    'boto3',
    'docker',
    'minio',
    'colorlog',
    # 'fsspec',
    'monai',
    'itk',
    'tqdm',
    'pandas',
    'matplotlib',
    'xnat',
    'GitPython',
    # 'protobuf~=3.19.0',
    'PyYAML',
    'requests',
    'click',
    'setuptools',
    # 'torch==1.13.0'
]

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
    dependency_links=[
            'https://download.pytorch.org/whl/torch_stable.html'
        ],
    entry_points={
        'console_scripts': [
            'mlops = mlops.cli:cli',
        ],
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
)
