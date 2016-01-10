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

# Test SimpleJob class.

import logging
import pprint
import testtools

import jenkins_manager.types.pipeline as pipeline
import jenkins_manager.types.job as job

import tests.base as base


class TestTriggerParameterizedBuildPipeline(base.LoggingFixture,
                                            testtools.TestCase):

    def test_initialize_from_list(self):
        """ Define a TestTriggerParameterizedBuildPipeline from a plain list of
        SimpleJob objects.
        """
        j = job.SimpleJob({
            "qualifier": "sweet",
            "name": "{{project}}__{{qualifier}}",
            "display-name": "{{project}} {{qualifier}} success",
        })
        h = job.SimpleJob({
            "qualifier": "bitter",
            "name": "{{project}}__{{qualifier}}",
            "display-name": "{{project}} {{qualifier}} success",
        })

        p = pipeline.TriggerParameterizedBuildPipeline([j, h])

        self.assertTrue((j in p))
        self.assertTrue((h in p))

    def test_jobs_connected(self):
        """ Show that on reification of the TriggerParameterizedBuildPipeline
        object, successive jobs become connected using the Trigger
        Parameterized Builds Jenkins plugin.
        """
        j = job.SimpleJob({
            "qualifier": "sweet",
            "name": "{{project}}__{{qualifier}}",
            "display-name": "{{project}} {{qualifier}} success",
        })
        h = job.SimpleJob({
            "qualifier": "bitter",
            "name": "{{project}}__{{qualifier}}",
            "display-name": "{{project}} {{qualifier}} success",
        })

        p = pipeline.TriggerParameterizedBuildPipeline()
        p.append(j)
        p.append(h)

        p.reify({
            "project": "meow",
        })
        logging.debug(pprint.pformat(p))

        self.assertEqual(
            j['publishers'][0]['trigger-parameterized-builds'][0]['project'],
            'meow__bitter')
