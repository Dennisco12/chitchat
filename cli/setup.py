from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="chitchatcli",
    version="0.0.3",
    author="Benjamin Eruvieru",
    author_email="benjamineruvieru@gmail.com",
    description="A command line chatting software designed for developers to communicate with each other.",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["python-socketio[client]",
                      'windows-curses==2.3.1; sys_platform == "win32"',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
