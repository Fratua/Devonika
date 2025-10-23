"""
Devonika - Full-Fledged AI Software Engineer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="devonika",
    version="0.1.0",
    author="Fratua",
    description="Full-fledged AI software engineer capable of building projects of any scale",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fratua/devonika",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.39.0",
        "aiofiles>=23.0.0",
        "rich>=13.0.0",
        "click>=8.1.0",
    ],
    extras_require={
        "dev": [
            "black>=24.0.0",
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
        ],
        "openai": [
            "openai>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "devonika=devonika.cli.main:main",
        ],
    },
)
