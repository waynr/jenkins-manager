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

# Test TemplateJob class.

import logging
import pprint
import testtools

import jenkins_manager.types.pipeline as pipeline
import jenkins_manager.types.job as job

import tests.base as base


class TestTriggerParameterizedBuildPipeline(base.LoggingFixture,
                                            testtools.TestCase):

    def setUp(self):
        super(TestTriggerParameterizedBuildPipeline, self).setUp()
        self.j1 = job.TemplateJob({
            "qualifier": "sweet",
            "name": "{{project}}__{{qualifier}}",
            "display-name": "{{project}} {{qualifier}} success",
        })
        self.j2 = job.TemplateJob(self.j1)
        self.j2["qualifier"] = "bitter"
        self.j3 = job.TemplateJob(self.j2)
        self.j3["qualifier"] = "sour"

    def test_initialize_from_list(self):
        """ Define a TestTriggerParameterizedBuildPipeline from a plain list of
        TemplateJob objects.
        """
        p = pipeline.TriggerParameterizedBuildPipeline([self.j1, self.j2])

        self.assertTrue((self.j1 in p))
        self.assertTrue((self.j2 in p))

    def test_jobs_connected(self):
        """ Show that on reification of the TriggerParameterizedBuildPipeline
        object, successive jobs become connected using the Trigger
        Parameterized Builds Jenkins plugin.
        """
        p = pipeline.TriggerParameterizedBuildPipeline()
        p.append(self.j1)
        p.append(self.j2)
        p.append(self.j3)

        p.render({
            "project": "meow",
        })
        logging.debug(pprint.pformat(p))

        tpb1 = self.j1.publishers[0]['trigger-parameterized-builds']
        tpb2 = self.j2.publishers[0]['trigger-parameterized-builds']
        self.assertEqual(
            tpb1[0]['project'],
            'meow__bitter')
        self.assertEqual(
            tpb2[0]['project'],
            'meow__sour')

    def test_default_tpb_settings(self):
        """ Validate default Trigger Paramterized Build settings.
        """
        p = pipeline.TriggerParameterizedBuildPipeline()
        p.append(self.j1)
        p.append(self.j2)

        p.render({
            "project": "meow",
        })

        correct_values = [
            ('fail-on-missing', True),
            ('current-parameters', True),
            ('trigger-with-no-params', True),
        ]

        tpb_params = self.j1.publishers[0]['trigger-parameterized-builds'][0]
        for param_name, correct_value in correct_values:
            self.assertEqual(tpb_params[param_name], correct_value)

    def test_custom_tpb_settings(self):
        """ Show that custom Trigger Parameterized Build settings can be
        defined when constructing the pipeline.
        """
        p = pipeline.TriggerParameterizedBuildPipeline()

        custom_tpb_values = [
            ('fail-on-missing', False),
            ('current-parameters', False),
            ('trigger-with-no-params', False),
            ('property-file', 'custom.props'),
        ]
        p.append((self.j1, custom_tpb_values))
        p.append(self.j2)

        p.render({
            "project": "meow",
        })

        tpb_params = self.j1.publishers[0]['trigger-parameterized-builds'][0]
        for param_name, correct_value in custom_tpb_values:
            self.assertEqual(tpb_params[param_name], correct_value)

    def test_multiple_downstreams(self):
        """ Show that custom Trigger Parameterized Build settings can be
        defined when constructing the pipeline.
        """
        p = pipeline.TriggerParameterizedBuildPipeline()
        p.append(self.j1)
        p.append([self.j2, self.j3])

        p.render({
            "project": "meow",
        })

        tpb1 = self.j1.publishers[0]['trigger-parameterized-builds']
        self.assertTrue('meow__bitter' in tpb1[0]['project'])
        self.assertTrue('meow__sour' in tpb1[0]['project'])

    def test_multiple_downstreams_followed_by_single(self):
        """ Show that custom Trigger Parameterized Build settings can be
        defined when constructing the pipeline.
        """
        j4 = job.TemplateJob(self.j3)
        j4['qualifier'] = 'salty'
        p = pipeline.TriggerParameterizedBuildPipeline()
        p.append(self.j1)
        p.append([self.j2, self.j3])
        p.append(j4)

        p.render({
            "project": "meow",
        })

        tpb1 = self.j1.publishers[0]['trigger-parameterized-builds']
        tpb2 = self.j2.publishers[0]['trigger-parameterized-builds']

        self.assertTrue('meow__bitter' in tpb1[0]['project'])
        self.assertTrue('meow__sour' in tpb1[0]['project'])
        self.assertTrue('meow__salty' in tpb2[0]['project'])
        self.assertTrue('publishers' not in self.j3)
