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

# Provide basic utility fuctions to share behaviour between modules.

import copy

import jinja2
from jinja2 import meta

import jenkins_manager.errors as errors


def render_dict(target_dict, override_dict, **kwargs):
    """ Use values found in target_dict, override_dict, and kwargs to populate
    jinja2 templates in the target_dict. This operation works in-place on the
    given target_dict.
    """
    dictcopy = copy.deepcopy(target_dict)

    if override_dict is not None:
        dictcopy.update(override_dict)

    if len(kwargs.keys()) != 0:
        dictcopy.update(kwargs)

    for key in target_dict:
        value = target_dict.pop(key)

        # Ensure that we have all the key/value pairs we need in the
        # mapping object we are applying to the key.
        env = jinja2.Environment()
        ast = env.parse(value)
        undeclared = meta.find_undeclared_variables(ast)

        missing_vars = [var for var in undeclared if var not in dictcopy]

        if missing_vars:
            raise errors.MissingTemplateVariableError(missing_vars, value)

        template = jinja2.Template(value)
        target_dict[key] = template.render(dictcopy)
