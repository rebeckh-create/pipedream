#!/usr/bin/env python3
"""
Setup script for Studio Automation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hiyoga-studio-automation",
    version="1.0.0",
    author="Studio Automation Team",
    description="Automated studio control system for recording sessions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        "Topic :: Multimedia :: Video :: Capture",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "studio-start=scripts.start_session:main",
            "studio-stop=scripts.stop_session:main", 
            "studio-status=scripts.studio_status:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml", "config/*.json"],
    },
)