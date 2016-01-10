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

import pprint


class MissingTemplateVariableError(Exception):

    def __init__(self, varlist, template_string=None):
        self.varlist = varlist
        self.template_string = template_string

    def __str__(self):
        if self.template_string is not None:
            string = """{0} is missing the following values: \n
            {1}
            """.format(self.template_string, pprint.pformat(self.varlist))
        else:
            string = """Missing the following values: \n
            {0}
            """.format(pprint.pformat(self.varlist))

        return string
