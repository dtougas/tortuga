# Copyright 2008-2018 Univa Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys

from tortuga.cli.base import RootCommand, Command
from tortuga.cli.utils import pretty_print


HISTORY_FILE = os.path.expanduser('~/.cache/tortuga')


class ListCommand(Command):
    """
    List command history.

    """
    name = 'list'
    help = 'List command history'

    def execute(self, args: argparse.Namespace):
        result = []

        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE) as fp:
                for line in fp.readlines():
                    line = line.strip()
                    #
                    # Remove blank lines
                    #
                    if not line:
                        continue
                    result.append(line.strip())

        pretty_print(result, args.fmt)


class ClearCommand(Command):
    """
    Clear command history.

    """
    name = 'clear'
    help = 'Clear command history'

    def execute(self, args: argparse.Namespace):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w') as fp:
                fp.write('')


class HistoryCommand(RootCommand):
    """
    Command for managing Tortuga CLI history.

    """
    name = 'history'
    help = 'Manage Tortuga CLI history'

    sub_commands = [
        ListCommand(),
        ClearCommand()
    ]

    def build_parser(self, parser: argparse.ArgumentParser):
        #
        # Register the command logger to be called after every command
        # execution
        #
        self.root.register_post_execute(self._log_command)
        super().build_parser(parser)

    def _log_command(self, _: argparse.Namespace):
        """
        Logs the command that was just run to the command history file.

        """
        history_dir = os.path.dirname(HISTORY_FILE)

        if not os.path.exists(history_dir):
            os.makedirs(history_dir)

        #
        # Don't log history commands
        #
        for arg in sys.argv:
            if arg.startswith('-'):
                continue

            elif arg == self.name:
                return

        with open(HISTORY_FILE, 'a') as fp:
            line = ' '.join(sys.argv)
            fp.write('{}\n'.format(line))
