import os
import platform
import sys

import pkg_resources
from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.dirname(__file__)
# The text of the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8", mode="r") as fd:
    README = fd.read()


requirements = []
if sys.platform.startswith("linux") and platform.machine() == "x86_64":
    requirements.append("triton==2.0.0")

setup(
    name="whisper",
    py_modules=["whisper"],
    version="1.0",
    description="Robust Speech Recognition via Large-Scale Weak Supervision",
    readme="README.md",
    python_requires=">=3.8",
    author="OpenAI",
    url="https://github.com/openai/whisper",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=requirements
    + [
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points={
        "console_scripts": ["whisper=whisper.transcribe:cli"],
    },
    include_package_data=True,
    extras_require={"dev": ["pytest", "scipy", "black", "flake8", "isort"]},
)
