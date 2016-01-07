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

import jenkins_jobs.xml_config as xml_config
import jenkins_jobs.registry as registry
import jenkins_jobs.config as jjb_config

from jenkins_manager.cli.subcommands import base
import jenkins_manager.loader


class DeploySubCommand(base.SubCommandBase):

    def parse_args(self, parser):
        deploy = parser.add_parser(
            'deploy',
            help="""Deploy jobs to jenkins instances.
            """
        )

        deploy.add_argument(
            'module_path',
            help="""Colon-separated list of paths to Python modules defining
            Jenkins jobs.
            """,
            nargs='?',
            default=None,
        )
        deploy.add_argument(
            'library_path',
            nargs='?',
            default=None,
        )

    def execute(self, config):
        module_path = config.arguments['module_path'].split(os.pathsep)
        library_path = config.arguments['library_path'].split(os.pathsep)
        logging.info(module_path)
        logging.info(library_path)

        loader = jenkins_manager.loader.PythonLoader(module_path, library_path)
        logging.debug(loader.jobs)

        jjbconfig = jjb_config.JJBConfig()
        module_registry = registry.ModuleRegistry(jjbconfig)
        xml_generator = xml_config.XmlJobGenerator(module_registry)

        xml_jobs = xml_generator.generateXML(loader.jobs)

        for xml_job in xml_jobs:
            logging.info(xml_job.output())
