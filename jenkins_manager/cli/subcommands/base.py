import abc
import six


@six.add_metaclass(abc.ABCMeta)
class SubCommandBase(object):
    """Base class for subcommands of cjc-manager.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_args(self, subparsers):
        """Provide argument parsing for the subcommand implementation.

        :param subparsers
          A sub parser object. Implementations of this method should
          create a new subcommand parser by calling
            subparsers.add_parser('command-name', ...)
          This will return a new ArgumentParser object; additional arguments to
          this method should provide ArgumentParser constructor arguments.
        """

    @abc.abstractmethod
    def execute(self, config):
        """The meat and potatoes of this subcommand, this is where all
        subcommand behavior should occur.

        :param config
          cjc-manager config object containing configuration from config files,
          command line arguments, and environment variables.
        """

    def parse_positional_jenkins_instance(self, parser):
        parser.add_argument(
            'jenkins_instance',
            metavar='JENKINS_INSTANCE',
            type=str,
            help='Jenkins instance against which to act with this command.')
