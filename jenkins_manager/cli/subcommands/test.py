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

# Jenkins Job Manager 'test' command

import sys

from jenkins_manager.cli.subcommands import deploy


class TestSubCommand(deploy.DeploySubCommand):

    def parse_args(self, parser):
        test = parser.add_parser(
            'test',
            help="""Test Jenkins Manager by dumping XML output to files at
            specified output directory, or if no output directory is specified
            then dump XML to stdout.
            """
        )
        test.add_argument('-o',
                          dest='output_dir',
                          default=sys.stdout,
                          help='path to output XML')

        self.parse_arg_module_path(test)
        self.parse_arg_library_path(test)

    def execute(self, config):
        xml_jobs, bldr = self._generate_jobs(config)
        jobs, num_updated_jobs = bldr.update_jobs(
            xml_jobs, n_workers=1, output=config.arguments['output_dir'])
