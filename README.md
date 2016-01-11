<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installing](#installing)
- [Using](#using)
    - [The `deploy` subcommand](#the-deploy-subcommand)
    - [The `test` subcommand](#the-test-subcommand)
- [Getting Help](#getting-help)

<!-- markdown-toc end -->

# Introduction

Jenkins Manager is an experimental API designed to allow users to construct
Jenkins jobs using the full power of the Python language. Jenkins Manager's API
is intended to generate a data structure compatible with Jenkins Job Builder's
(JJB) XmlGenerator object in order to produce valid Jenkins job configurations.

# Requirements

* Python version 2.7 or 3.4
* Jenkins Job Builder 2.x

**Note** Because versions of JJB less than 2.x do not provide XML generation
  separate from job definition via YAML, Jenkins Manager will only work on JJB
  2.x and later. Because JJB 2.x is still awainting review by review its core
  developers, users of Jenkins Manager should consider the tool and the API as
  unstable until the its first "0.0.0" release to Pypi.

# Installing

Because both Jenkins Job Builder 2.x and Jenkins Manager are still under
development, you will have to install both from their respective git
repositories.

```bash
$ git clone http://github.com/waynr/jenkins-manager
$ cd jenkins-manager
$ git clone -b jjb-2.0.0-api http://github.com/waynr/jenkins-job-builder
$ virtualenv .virtualenv && source .virtualenv/bin/activate
$ pip install -e jenkins-job-builder
$ pip install -e ./
```

# Using

Jenkins Manager comes with a relatively simple tool called `jankman`:

```bash
$ jankman -h
usage: jankman [-h] [--conf CONF] [-l LOG_LEVEL] [--use-cache]
               {test,deploy} ...

positional arguments:
  {test,deploy}
    test                Test Jenkins Manager by dumping XML output to files at
                        specified output directory, or if no output directory
                        is specified then dump XML to stdout.
    deploy              Deploy jobs to jenkins instances.

optional arguments:
  -h, --help            show this help message and exit
  --conf CONF           configuration file
  -l LOG_LEVEL, --log_level LOG_LEVEL
                        log level (default: info)
  --use-cache           ignore the cache and update the jobs anyhow (that will
                        only flush the specified jobs cache)
```

This tool comes with two subcommands, `test`, and `deploy`.

## The `deploy` subcommand

```bash
$ jankman deploy -h
usage: jankman deploy [-h] module_path [library_path]

positional arguments:
  module_path   Colon-separated list of paths to Python modules defining
                Jenkins jobs.
  library_path  Colon-separated list of paths to search for user-defined
                libraries. Note that this should only be necessary if users
                define libraries somewhere outside the module_path.

optional arguments:
  -h, --help    show this help message and exit
```

This command takes a mandatory path argument that must point to a directory
containing Python modules. For each module it finds, if that module has a
`get_jobs` function, it will treat the return value of that module as if it were
a `list of dictionaries` and pass them to JJB's `XmlGenerator.generateXML`
method in order to generate Jenkins job XML configuration. It will then use JJB
to upload these job configurations to the Jenkins instances specified by the
configuration specified with the primary command's `--conf' argument.

## The `test` subcommand

```bash
$ jankman test -h
usage: jankman test [-h] [-o OUTPUT_DIR] module_path [library_path]

positional arguments:
  module_path    Colon-separated list of paths to Python modules defining
                 Jenkins jobs.
  library_path   Colon-separated list of paths to search for user-defined
                 libraries. Note that this should only be necessary if users
                 define libraries somewhere outside the module_path.

optional arguments:
  -h, --help     show this help message and exit
  -o OUTPUT_DIR  path to output XML
```

This command is almost identical to `deploy` with one crucial difference;
namely, it does not upload job configurations to a Jenkins instance. Instead, by
default it will print the pretty-fied XML for all generated jobs to `STDOUT`.
Alternative, if the `-o` argument is given, it will create the specified
directory if it does not already exist and write one XML file per generated job
in that directory with the job's name as it would show up in its Jenkins URL as
the name of the file.

# Getting Help

I usually hang out in the `#openstack-infra` channel on irc.freenode.net under
the nickname `waynr`; ping me there if you have questions or file a Github Issue
here if you have trouble with the command line tool or API.
