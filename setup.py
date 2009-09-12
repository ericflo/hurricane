#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="hurricane",
    version="0.1",
    description="Hurricane is a project for easily creating Comet web applications",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Environment :: Web Environment",
    ],
    keywords="comet,asynchronous,messages,messaging,framework",
    author="The Hurricane Development Team",
    author_email="floguy+hurricane@gmail.com",
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url="http://github.com/ericflo/hurricane",
)
