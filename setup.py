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
        "Development Status :: 1 - Planning",
        ],
    packages=[
        "benterfaces",
        ],
    install_requires=[
        "zope.interface",
        ],
    )
