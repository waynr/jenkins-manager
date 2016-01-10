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

import jinja2
from jinja2 import meta
import six

import jenkins_manager.errors as errors


@six.add_metaclass(abc.ABCMeta)
class Job(dict):
    """Base class for Jenkins jobs, defines method interface
    """

    @abc.abstractmethod
    def reify(self, extra_dict=None, **kwargs):
        """Subclasses that define template attributes must provide an
        implementation of this function that will populate those templates with
        values available on the subclass. This method may also take an optional
        mapping object to provide additional values.
        """
        raise NotImplementedError


class SimpleJob(Job):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)

    def reify(self, override_dict=None, **kwargs):
        dictcopy = copy.deepcopy(self)

        if override_dict is not None:
            dictcopy.update(override_dict)

        if len(kwargs.keys()) != 0:
            dictcopy.update(kwargs)

        for key in self:
            value = self.pop(key)

            # Ensure that we have all the key/value pairs we need in the
            # mapping object we are applying to the key.
            env = jinja2.Environment()
            ast = env.parse(value)
            undeclared = meta.find_undeclared_variables(ast)

            missing_vars = [var for var in undeclared if var not in dictcopy]

            if missing_vars:
                raise errors.MissingTemplateVariableError(missing_vars, value)

            template = jinja2.Template(value)
            self[key] = template.render(dictcopy)

        self = dictcopy
