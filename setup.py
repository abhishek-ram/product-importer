import io

from setuptools import find_packages, setup

with io.open('README.md', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='product_importer',
    version='1.0.0',
    url='',
    description='Application to Import and Manage Products',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django==2.1.7',
    ],
    extras_require={},
    scripts=['manage.py']
)
