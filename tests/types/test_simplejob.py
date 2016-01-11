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

import testtools

import jenkins_manager.types.job as job
import jenkins_manager.errors as errors


class TestTemplateJob(testtools.TestCase):

    def setUp(self):
        super(TestTemplateJob, self).setUp()

    def test_initialize_from_dict(self):
        """ Validate that a TemplateJob instance may be initialized with a single
        dictionary argument by checking that all keys in the given dict can be
        found in the resulting TemplateJob.
        """
        d = {
            'key1': 'value1',
            'key2': 'value2',
        }
        j = job.TemplateJob(d)
        self.assertEqual(d, j)

    def test_initialize_from_kwargs(self):
        """ Validate that a TemplateJob instance may be initialized using keyword
        arguments on its constructor. Check that all keywords and their values
        can be found in the resulting TemplateJob.
        """
        d = dict(key1='value1', key2='value2')
        j = job.TemplateJob(key1='value1', key2='value2')
        self.assertEqual(d, j)

    def test_render_from_dict(self):
        """ Validate that a TemplateJob instance may be reified using .render()
        passed a dictionary argument.
        """
        d = {
            'project': 'puppet-server',
            'gitbranch': 'master',
        }

        j = job.TemplateJob({
            'name': '{{project}}__test__{{gitbranch}}',
            'display-name': '({{project}}) [{{gitbranch}}]',
        })
        j.render(d)

        self.assertEqual(j, {
            'name': 'puppet-server__test__master',
            'display-name': '(puppet-server) [master]',
        })

    def test_render_from_kwargs(self):
        """ Validate that a TemplateJob instance may be reified using .render()
        passed keyword arguments.
        """
        j = job.TemplateJob({
            'name': '{{project}}__test__{{gitbranch}}',
            'display-name': '({{project}}) [{{gitbranch}}]',
        })
        j.render(
            project='puppet-server',
            gitbranch='master',
        )

        self.assertEqual(j, {
            'name': 'puppet-server__test__master',
            'display-name': '(puppet-server) [master]',
        })

    def test_render_with_missing_vars(self):
        """ If we are missing variables, users must be notified.
        """
        j = job.TemplateJob({
            'name': '{{project}}__test__{{gitbranch}}',
            'display-name': '({{project}}) [{{gitbranch}}]',
        })

        # We must have all variables available
        with testtools.ExpectedException(errors.MissingTemplateVariableError):
            j.render(
                project='puppet-server',
            )
