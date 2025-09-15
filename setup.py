from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent

# Read the README for a nice long description if present
readme_path = ROOT / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else "DoneDeal scraping utilities"

# Parse requirements from requirement.txt if available
req_path = ROOT / "requirement.txt"
if req_path.exists():
    install_requires = [
        line.strip()
        for line in req_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
else:
    install_requires = []

setup(
    name="donedeal",
    version="0.1.0",
    description="A simple scraper and utilities for DoneDeal car listings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="",
    url="",
    packages=find_packages(exclude=("tests", "media", "curve_fitting")),
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={
        "console_scripts": [
            "donedeal=donedeal.__main__:main",
        ]
    },
)