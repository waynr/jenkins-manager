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

# Jenkins Job Manager 'deploy' command

import logging
import os
import pprint

import jenkins_jobs.xml_config as xml_config
import jenkins_jobs.registry as registry
import jenkins_jobs.builder as builder
import jenkins_jobs.config as jjb_config

from jenkins_manager.cli.subcommands import base
import jenkins_manager.loader


class DeploySubCommand(base.SubCommandBase):

    def parse_arg_module_path(self, parser):
        parser.add_argument(
            'module_path',
            help="""Colon-separated list of paths to Python modules defining
            Jenkins jobs.
            """,
        )

    def parse_arg_library_path(self, parser):
        parser.add_argument(
            'library_path',
            help="""Colon-separated list of paths to search for user-defined
            libraries. Note that this should only be necessary if users define
            libraries somewhere outside the module_path.
            """,
            nargs='?',
            default=None,
        )

    def parse_args(self, parser):
        deploy = parser.add_parser(
            'deploy',
            help="""Deploy jobs to jenkins instances.
            """
        )
        self.parse_arg_module_path(deploy)
        self.parse_arg_library_path(deploy)

    def _generate_jobs(self, config):
        module_path = config.arguments['module_path'].split(os.pathsep)

        library_path = config.arguments['library_path']
        if library_path is not None:
            library_path = library_path.split(os.pathsep)

        logging.debug("Module path: {0}".format(module_path))
        logging.debug("Library path: {0}".format(library_path))

        loader = jenkins_manager.loader.PythonLoader(module_path, library_path)
        logging.debug("Jobs loaded: {0}".format(pprint.pformat(loader.jobs)))

        jjbconfig = jjb_config.JJBConfig(config.arguments['conf'])
        jjbconfig.do_magical_things()
        jjbconfig.builder['ignore_cache'] = (not config.arguments['use_cache'])

        bldr = builder.Builder(jjbconfig)
        module_registry = registry.ModuleRegistry(jjbconfig, bldr.plugins_list)
        xml_generator = xml_config.XmlJobGenerator(module_registry)

        xml_jobs = xml_generator.generateXML(loader.jobs)

        return xml_jobs, bldr

    def execute(self, config):
        xml_jobs, bldr = self._generate_jobs(config)
        jobs, num_updated_jobs = bldr.update_jobs(xml_jobs, n_workers=1)
