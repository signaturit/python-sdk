from distutils.core import setup
import os

setup(
    author = 'Signaturit',
    author_email = 'api@signaturit.com',
    description = "Signaturit Python SDK",
    install_requires = ['requests', 'httpretty'],
    keywords = "signaturit e-signature python sdk",
    license = 'MIT',
    name = 'signaturit_sdk',
    packages = ['signaturit_sdk', 'signaturit_sdk.tests', 'signaturit_sdk.resources'],
    url = 'https://github.com/signaturit/python-sdk',
    version = '1.1.0'
)
