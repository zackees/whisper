import os
import sys

import pkg_resources
from setuptools import find_packages, setup

# The directory containing this file
HERE = os.path.dirname(__file__)
# The text of the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8", mode="r") as fd:
    README = fd.read()


requirements = []
if sys.platform.startswith("linux"):
    triton_requirement = "triton>=2.0.0.dev20221202"
    try:
        import re
        import subprocess

        version_line = (
            subprocess.check_output(["nvcc", "--version"]).strip().split(b"\n")[-1]
        )
        major, minor = re.findall(rb"([\d]+)\.([\d]+)", version_line)[0]
        if (int(major), int(minor)) < (11, 4):
            # the last version supporting CUDA < 11.4
            triton_requirement = "triton==2.0.0.dev20221011"
    except (IndexError, OSError, subprocess.SubprocessError):
        pass
    requirements.append(triton_requirement)

setup(
    name="whisper",
    py_modules=["whisper"],
    version="1.0",
    description="Robust Speech Recognition via Large-Scale Weak Supervision",
    readme="README.md",
    python_requires=">=3.7",
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
