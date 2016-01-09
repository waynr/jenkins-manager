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

# Define basic jenkins job abstractions.

import abc

import six
import jenkins_jobs.formatter as formatter


@six.add_metaclass(abc.ABCMeta)
class Job(dict):
    """Base class for Jenkins jobs, defines method interface
    """

    @abc.abstractmethod
    def reify(self, extra_dict=None):
        """Subclasses that define template attributes must provide an
        implementation of this function that will populate those templates with
        values available on the subclass. This method may also take an optional
        mapping object to provide additional values.
        """
        raise NotImplementedError


class JobName(object):
    def __init__(self, **kwargs):
        pass


class SimpleJob(Job):

    _name_template = '{value-stream}__{project-name}__{qualifier}'
    _display_name_template = '({project-name})'

    template_keys = [
        'project-name',
        'value-stream',
        'qualifier',
    ]

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)

    def reify(self):
        if 'name' not in self or len(self['name']) == 0:
            self['name'] = formatter.deep_format(self._name_template, self)

        if 'display-name' not in self or len(self['display-name']) == 0:
            self['display-name'] = formatter.deep_format(
                self._display_name_template, self)

        for key in self:
            value = self.pop(key)
            self[key] = formatter.deep_format(value, self)
