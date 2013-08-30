# Description:
#   example module
#
# Commands:
#
#   !example - run default function
#   !example subcommand - run subcommand function
#   !example subcommand_args <arguments> - run sample command that takes a list #       of arguments
#
from botulus.basemodule import BaseModule


class Example(BaseModule):
    def default(self):
        return 'This is ran when the example module is called with no args'

    def subcommand(self):
        return 'A normal subcommand function that takes no arguments'

    def subcommand_with_args(self, args=None):
        msg = 'This function gets a list of arguments, you provided %s'
        return msg % len(args)

__module__ = Example
