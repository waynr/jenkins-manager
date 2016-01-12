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

# Test the utils.render() function.

import testtools

from jenkins_manager import utils
from tests import base


class TestRender(base.LoggingFixture, testtools.TestCase):

    def test_render_string(self):
        """ Test that utils.render will correctly render a string template.
        """
        s = utils.render("{{value}}", {"value": "hello"})
        self.assertEquals("hello", s)

    def test_render_list(self):
        """ Test that utils.render will correctly render a list of string
        templates and ignore strings without template variables.
        """
        ts = [
            "{{value1}}",
            "{{value2}}",
            "foobar",
        ]
        s = utils.render(ts, {"value1": "hello", "value2": "meow"})
        self.assertEquals(["hello", "meow", "foobar"], s)

    def test_render_dictionary(self):
        """ Test that utils.render will correctly render the values in a
        dictionary.
        """
        ds = {
            "key1": "{{value1}}",
            "key2": "{{value2}}",
            "key3": "foobar",
        }
        s = utils.render(ds, {"value1": "hello", "value2": "meow"})
        self.assertEquals({
            "key1": "hello",
            "key2": "meow",
            "key3": "foobar"}, s)

    def test_render_list_of_dictionaries(self):
        """ Test that utils.render will correctly render a list of
        dictionaries.
        """
        ds = {
            "key1": "{{value1}}",
            "key2": "{{value2}}",
            "key3": "foobar",
        }
        ts = [ds, dict(ds)]
        s = utils.render(ts, {"value1": "hello", "value2": "meow"})
        self.assertEquals([{
            "key1": "hello",
            "key2": "meow",
            "key3": "foobar"}, {
            "key1": "hello",
            "key2": "meow",
            "key3": "foobar"}], s)
