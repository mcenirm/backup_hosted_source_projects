#!/usr/bin/env python

from setuptools import setup


setup(
    author='Michael McEniry',
    author_email='mcenirm@uah.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2.6',
    ],
    description='Backup source projects hosted on various services',
    entry_points={
        'console_scripts': [
            'backup_hosted_source_projects=backup_hosted_source_projects:main',
        ],
    },
    install_requires=[
        'pygithub3>=0.5.1',
        'python-gitlab>=0.13',
    ],
    license='GPL',
    name='backup_hosted_source_projects',
    py_modules=[
        'backup_hosted_source_projects'
    ],
    url='https://github.com/mcenirm/backup_hosted_source_projects',
    version='0.0.1',
)
