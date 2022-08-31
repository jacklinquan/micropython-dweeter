import sys

# Remove current dir from sys.path, otherwise setuptools will peek up our
# module instead of system's.
sys.path.pop(0)
from setuptools import setup

sys.path.append("./sdist_upip")
import sdist_upip

setup(
    name="micropython-dweeter",
    version="0.2.0",
    description="A python module for messaging through the free dweet service.",
    long_description="https://github.com/jacklinquan/micropython-dweeter",
    long_description_content_type="text/markdown",
    url="https://github.com/jacklinquan/micropython-dweeter",
    author="Quan Lin",
    author_email="jacklinquan@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
    cmdclass={"sdist": sdist_upip.sdist},
    py_modules=["dweeter"],
    install_requires=["micropython-cryptodweet"],
)
