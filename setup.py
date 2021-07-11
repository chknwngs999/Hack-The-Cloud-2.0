import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htc-2-0-pkg-chknwngs999",
    version="0.0.1",
    author="Ryan Lee",
    author_email="ryanlee4761@gmail.com",
    description="Package for Hack the Cloud 2.0 COVID Data Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chknwngs999/Hack-The-Cloud-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "flaskr"},
    packages=setuptools.find_packages(where="flaskr"),
    python_requires=">=3.6",
)

#follow steps here https://packaging.python.org/tutorials/packaging-projects/ except for twine + after