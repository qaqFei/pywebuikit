import setuptools

import pywebuikit

setuptools.setup(
    name = "pywebuikit",
    version = f"{pywebuikit.__version__}",
    description = "A Python package for creating web applications with a simple and easy-to-use API.",
    long_description = open("README.md", "r", encoding="utf-8").read(),
    author = "qaqFei",
    author_email = "qaq_fei@163.com",
    url = "https://github.com/qaqFei/pywebuikit",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows"
    ],
    install_requires = ["pywebview==5.2"],
    license = "MIT License",
    python_requires = ">=3.12.0"
)