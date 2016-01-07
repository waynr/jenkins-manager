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

# Job loading classes

import collections
import importlib
import inspect
import logging
import pprint
import os
import sys


def find_and_load_modules(module_path, library_path=None):
    """
    Given a list of paths, recurse into those paths, load all python modules
    found, and return those that contain functions pertinent to JJB data
    structure loading.
    """

    modules = [m for m in __load_modules(module_path) if __is_valid(m)]

    return modules


def __load_modules(module_path, library_path=None):
    loaded_modules = []
    module_files = []

    for dirpath, dirnames, filenames in os.walk(module_path):
        relative_path = os.path.relpath(dirpath, module_path)
        if relative_path == ".":
            relative_path = ""
        for filename in filenames:
            name, ext = os.path.splitext(filename)
            if (ext == ".py" and not name == "__init__"):
                relative_path = ".".join(relative_path.split("/"))
                if relative_path == "":
                    module_files.append(name)
                else:
                    module_files.append(relative_path + "." + name)

    sys.path.insert(0, module_path)
    if library_path is not None:
        sys.path.insert(0, library_path)

    logging.debug(pprint.pformat(sys.path))
    for module_file in module_files:
        tmp = importlib.import_module(module_file)
        logging.debug("Loaded {0}".format(tmp))
        loaded_modules.append(tmp)

    # avoid accidentially prioritizing some module in the jobs module path over
    # those defined elsewhere
    sys.path.remove(module_path)

    return loaded_modules


def __is_valid(module):
    """
    Perform basic validity check to ensure that the given module is compatible
    with the expectations we have for modules which generate JJB data
    structures.
    """

    if not inspect.ismodule(module):
        return False

    members = collections.OrderedDict(inspect.getmembers(module))

    if "get_jobs" not in members:
        return False

    return True


class PythonLoader(object):

    def __init__(self, module_paths, library_paths=None):
        self.__module_paths = module_paths
        self.__library_paths = library_paths
        self.__loaded_modules = None
        self.__jobs = None

    def __load_modules(self, module_paths, library_paths=None):
        modules = []
        for module_path in module_paths:
            modules.extend(find_and_load_modules(module_path, library_paths))
        return modules

    @property
    def modules(self):
        if self.__loaded_modules is None:
            logging.info("Loading modules from path: {0}".format(
                self.__module_paths))
            self.__loaded_modules = self.__load_modules(
                self.__module_paths,
                self.__library_paths
            )
        logging.info("Modules loaded.")
        return self.__loaded_modules

    def __get_jobs(self):
        jobs = []
        for module in self.modules:
            jobs.extend(module.get_jobs())
        return jobs

    @property
    def jobs(self):
        if self.__jobs is None:
            self.__jobs = self.__get_jobs()
        return self.__jobs
