#!/usr/bin/env python

from setuptools import setup

setup(name="const",
      version="0.1",
      license="MIT",
      description="Define constants and enums for Python",
      long_description=open("README.md", "r").read(),
      author="Zsolt Cserna",
      author_email="cserna.zsolt@gmail.com",
      url="http://www.github.com/csernazs/const",
      test_suite="test",
      packages=["const"],
      package_dir={"": "lib"},
      keywords=["enum", "constant", "const"],
      classifiers=[
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Developers",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
                "Programming Language :: Python :: 2",
                ],
     )
     
     