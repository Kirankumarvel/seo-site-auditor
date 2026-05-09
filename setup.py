#!/usr/bin/env python
"""Setup configuration for SEO Auditor"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="seo-auditor",
    version="1.0.0",
    author="Kiran",
    description="Automated SEO Site Auditor for comprehensive website analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/seo-auditor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
        "beautifulsoup4>=4.11.0",
        "click>=8.1.0",
        "lxml>=4.9.0",
    ],
    entry_points={
        "console_scripts": [
            "seo-auditor=seo_auditor.cli:cli",
        ],
    },
)
