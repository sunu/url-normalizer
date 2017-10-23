#!/usr/bin/env python
from setuptools import setup

setup(
    name="url-normalizer",
    version="0.0.1",
    author="Tarashish Mishra",
    author_email="sunu@sunu.in",
    description="Normalize URLs. Mostly useful for deduplicating HTTP URLs.",
    long_description="",
    license="MIT",
    url="https://github.com/sunu/url-normalizer",
    packages=['normalizer'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
