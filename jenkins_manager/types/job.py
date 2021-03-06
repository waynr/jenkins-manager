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
import copy

import six

from jenkins_manager import utils


@six.add_metaclass(abc.ABCMeta)
class Job(dict):
    """Base class for Jenkins jobs, defines method interface
    """

    valid_module_types = [
        'builders',
        'metadata',
        'notifications',
        'parameters',
        'properties',
        'publishers',
        'reporters',
        'scm',
        'triggers',
        'wrappers',
    ]

    def __get_module_class(self, name):
        if hasattr(self, name):
            return self.__getitem__(name)
        return None

    def __getattr__(self, name):
        if name in self.valid_module_types:
            return self.__get_module_class(name)

        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name in self.valid_module_types:
            self.__setitem__(name, value)

    @abc.abstractmethod
    def render(self, extra_dict=None, **kwargs):
        """Subclasses that define template attributes must provide an
        implementation of this function that will populate those templates with
        values available on the subclass. This method may also take an optional
        mapping object to provide additional values.
        """
        raise NotImplementedError


class TemplateJob(Job):

    def __init__(self, *args, **kwargs):
        super(TemplateJob, self).__init__(*args, **kwargs)

    def render(self, override_dict=None, **kwargs):
        dictcopy = copy.deepcopy(self)
        if override_dict is not None:
            dictcopy.update(override_dict)

        if len(kwargs.keys()) != 0:
            dictcopy.update(kwargs)

        return utils.render(self, dictcopy)
