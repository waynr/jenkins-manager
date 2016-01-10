#!/usr/bin/env python

import setuptools

try:
    from setupext import janitor
    CleanCommand = janitor.CleanCommand
except ImportError:
    CleanCommand = None

cmd_classes = {}
if CleanCommand is not None:
    cmd_classes['clean'] = CleanCommand

__MAJOR__ = 0
__MINOR__ = 0
__PATCH__ = 1
__QUALIFIER__ = "dev"

VERSION = "{0}.{1}.{2}".format(__MAJOR__,
                               __MINOR__,
                               __PATCH__) + __QUALIFIER__

setuptools.setup(
    author="Wayne Warren",

    name="jankman",
    author_email="waynr+launchpad@sdf.org",
    license="Apache License, Version 2.0",
    url="https://github.com/waynr/jenkins-manager",

    version=VERSION,

    entry_points={
        'console_scripts': [
            'jankman = jenkins_manager.cli.entry:main',
        ],
        'jenkins_manager.cli.subcommands': [
            'deploy = jenkins_manager.cli.subcommands.deploy:DeploySubCommand',
            'test = jenkins_manager.cli.subcommands.test:TestSubCommand',
        ],
    },

    classifiers=[
        'Topic :: Utilities',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3'
    ],

    install_requires=[
        "argparse",
        "jinja2",
        "six>=1.5.2,<2.0",
        "stevedore==1.8.0",
    ],

    cmdclass=cmd_classes,
)
