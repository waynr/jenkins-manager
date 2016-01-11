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

import jinja2
from jinja2 import meta

import jenkins_manager.errors as errors


def render_dict(obj, param_dict):
    """ Use values found in obj, param_dict, and kwargs to populate jinja2
    templates in the obj. This operation works in-place on the given obj.
    """
    if isinstance(obj, list):
        for i, item in enumerate(obj):
            obj[i] = render_dict(item, param_dict)
    elif isinstance(obj, dict):
        for item in obj:
            obj[item] = render_dict(obj[item], param_dict)
    elif isinstance(obj, basestring):
        # Ensure that we have all the key/value pairs we need in the
        # mapping object we are applying to the key.
        env = jinja2.Environment()
        ast = env.parse(obj)
        undeclared = meta.find_undeclared_variables(ast)

        missing_vars = [var for var in undeclared if var not in param_dict]

        if missing_vars:
            raise errors.MissingTemplateVariableError(missing_vars, obj)

        template = jinja2.Template(obj)
        return template.render(param_dict)

    return obj
