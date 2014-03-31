from setuptools import setup

setup(
    author='Judit Acs',
    author_email='judit@sch.bme.hu',
    name='wikt2dict',
    provides=['wikt2dict'],
    url='https://github.com/juditacs/wikt2dict',
    packages=['wikt2dict'],
    package_dir={'': '.'},
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=['docopt'],
    scripts=['wikt2dict/w2d.py'],
)
