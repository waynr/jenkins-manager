#!/usr/bin/env python
# Copyright (C) 2016 Wayne Warren
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# Command line entry point for jankman command line tool.

import argparse
import logging
import sys

from stevedore import extension


logging.basicConfig(
    format='%(levelname)s:%(module)s:%(message)s',
    level=logging.INFO,
)


class JMConfig(object):
    def __init__(self, arguments_dict):
        self.arguments = arguments_dict
        self.__config_parser = None

    @property
    def config_parser(self):
        # if self.__config_parser is None:
        pass


class Jankman(object):
    """ Entry point class for the 'jankman' command line tool.
    """

    def __init__(self, args):
        parser = self.create_parser()
        arguments = parser.parse_args(args)

        if (arguments.log_level is not None):
            arguments.log_level = getattr(logging,
                                          arguments.log_level.upper(),
                                          'INFO')
            logger = logging.getLogger()
            logger.setLevel(arguments.log_level)
            logging.debug("hello")

        self.jm_config = JMConfig(vars(arguments))

    def create_parser(self):
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--conf',
            dest='conf',
            default=None,
            help='configuration file'
        )
        parser.add_argument(
            '-l',
            '--log_level',
            dest='log_level',
            default='info',
            help="log level (default: %(default)s)"
        )
        parser.add_argument(
            '--use-cache',
            action='store_true',
            dest='use_cache',
            default=False,
            help='ignore the cache and update the jobs anyhow (that will only '
            'flush the specified jobs cache)'
        )
        # parser.add_argument(
        #     '--flush-cache',
        #     action='store_true',
        #     dest='flush_cache',
        #     default=False,
        #     help='flush all the cache entries before updating'
        # )
        # parser.add_argument(
        #     '--version',
        #     dest='version',
        #     action='version',
        #     version=__version__(),
        #     help='show version'
        # )

        subparser = parser.add_subparsers(
            # help='deploy jenkins configuration',
            dest='command'
        )

        extension_manager = extension.ExtensionManager(
            namespace='jenkins_manager.cli.subcommands',
            invoke_on_load=True,
        )

        def parse_subcommand_args(ext, subparser):
            ext.obj.parse_args(subparser)

        extension_manager.map(parse_subcommand_args, subparser)

        return parser

    def execute(self):
        arguments = self.jm_config.arguments

        extension_manager = extension.ExtensionManager(
            namespace='jenkins_manager.cli.subcommands',
            invoke_on_load=True,)

        ext = extension_manager[arguments['command']]
        ext.obj.execute(self.jm_config)
        pass


def main():
    argv = sys.argv[1:]
    j = Jankman(argv)
    j.execute()


if __name__ == '__main__':
    main()
