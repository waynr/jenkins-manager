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

# Define basic jenkins job collections

import abc

import six


@six.add_metaclass(abc.ABCMeta)
class Pipeline(list):
    """Base class for collections of Jenkins jobs, represented as a
    MutableSequence (list).
    """

    @abc.abstractmethod
    def reify(self, override_dict=None, **kwargs):
        """Subclasses that define template attributes must provide an
        implementation of this function that will populate those templates with
        values available on the subclass. This method may also take an optional
        mapping object to provide additional values.
        """
        raise NotImplementedError


class TriggerParameterizedBuildPipeline(Pipeline):

    def __init__(self, *args, **kwargs):
        super(TriggerParameterizedBuildPipeline, self).__init__(*args,
                                                                **kwargs)
        self.__jobs = []
        self.__reified = False

    def __connect_jobs(self, upstream, downstream):
        downstream_name = downstream['name']

        trigger = {
            'project': downstream_name,
            'fail-on-missing': True,
            'current-parameters': True,
            'trigger-with-no-params': True,
        }
        if 'publishers' in upstream:
            publishers = [publisher.keys()[0]
                          for publisher in upstream.publishers]
        else:
            upstream['publishers'] = [
                {'trigger-parameterized-builds': [trigger]}
            ]
            return

        tpb_i = None
        for i, publisher in enumerate(publishers):
            if publisher == 'trigger-parameterized-builds':
                tpb_i = i
                break

        if tpb_i:
            pub = upstream.publishers
            pub[tpb_i]['trigger-parameterized-builds'].append(trigger)

    def reify(self, override_dict=None, **kwargs):
        for job in self:
            job.reify(override_dict, **kwargs)

        # now that jobs know their names (which they may not have before if
        # they were template strings), connect them using the Trigger
        # Parameterized Build plugin.
        for i, job in enumerate(self[:-1]):
            self.__connect_jobs(job, self.__getitem__(i + 1))

        self.__reified = True
