from distutils.core import setup

setup(
    name='pepe-ipfs',
    version='0.1.0',
    long_description=open('README.md').read(),
    install_requires=[
        "requests>=2.24.0",
        "requests-toolbelt>=0.9.1"
    ]
)
