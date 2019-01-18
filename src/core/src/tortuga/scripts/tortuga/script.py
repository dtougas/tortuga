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
import logging
import os
import sys

from tortuga.cli.base import Argument, Cli
from tortuga.cli.exceptions import SkipExecution
from tortuga.config.configManager import ConfigManager
from tortuga.logging import CLI_NAMESPACE, ROOT_NAMESPACE


logger = logging.getLogger(CLI_NAMESPACE)


class TortugaScript(Cli):
    """
    The Tortuga Cli implementation.

    """
    command_package = 'tortuga.scripts.tortuga.commands'


    arguments = [
        Argument(
            '-v', '--version',
            action='store_true',
            dest='version',
            default=False,
            help='print version and exit'
        ),
        Argument(
            '-d', '--debug',
            dest='debug',
            help='set debug level; valid values are: critical, error, '
                 'warning, info, debug'
        ),
        Argument(
            '--url',
            help='Web service URL'
        ),
        Argument(
            '--username',
            dest='username',
            help='Web service user name'
        ),
        Argument(
            '--password',
            dest='password',
            help='Web service password'
        ),
        Argument(
            '--no-verify',
            dest='verify',
            default=True,
            action='store_false',
            help="Don't verify the API SSL certificate"
        ),
        Argument(
            '--json',
            dest='fmt',
            default='yaml',
            action='store_const',
            const='json',
            help='Output as JSON',
        )
    ]

    def build_parser(self, parser: argparse.ArgumentParser):
        self.register_pre_execute(self._version)
        self.register_pre_execute(self._set_log_level)
        super().build_parser(parser)

    def _version(self, args: argparse.Namespace):
        """
        Implements the --version argument.

        """
        if args.version:
            cm = ConfigManager()

            print(
                '{0} version: {1}'.format(
                    os.path.basename(sys.argv[0]),
                    cm.getTortugaRelease()
                )
            )

            #
            # Don't bother doing any command execution
            #
            raise SkipExecution()

    def _set_log_level(self, args: argparse.Namespace):
        """
        Implements the --debug argument.

        """
        if args.debug:
            root_logger = logging.getLogger(ROOT_NAMESPACE)
            root_logger.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            ch.setFormatter(formatter)
            root_logger.addHandler(ch)


def main():
    """
    Main.

    """
    TortugaScript().run()
