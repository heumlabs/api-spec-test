from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="api-spec-test",
    version="0.0.1",
    author="Sangmin Kang",
    author_email="ksmin@heumlabs.io",
    description="A python REST API test library that tests based on API specification.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/heumlabs/api-spec-test",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # install_requires=requirements,
)
