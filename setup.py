from distutils.core import setup

setup(
    name='cloudant-compliance-checks',
    version='0.1dev',
    packages=['compliance', 'compliance.utils'],
    license='IBM internal use only',
    long_description=open('README.md').read(),
)
