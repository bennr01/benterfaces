"""setup.py for benterfaces"""

from setuptools import setup


setup(
    name="benterfaces",
    version="0.0.1",
    author="bennr01",
    author_email="benjamin99.vogt@web.de",
    description="interface utilities",
    long_description=open("README.md").read(),
    license="MIT",
    keywords="interface interfaces utilities",
    url="https://github.com/bennr01/benterfaces/",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ],
    packages=[
        "benterfaces",
        ],
    install_requires=[
        "zope.interface",
        ],
    )
