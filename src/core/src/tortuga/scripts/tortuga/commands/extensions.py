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
import io
import subprocess
from typing import List
from xml.etree.ElementTree import ElementTree

import requests

from tortuga.cli.base import RootCommand, Command, Argument
from tortuga.cli.utils import pretty_print
from tortuga.config.configManager import ConfigManager
from .tortuga_ws import get_web_service_config


class ListCommand(Command):
    """
    List available extensions.

    """
    name = 'list'
    help = 'List available extensions'

    def execute(self, args: argparse.Namespace):
        pretty_print(get_available_extensions(args), args.fmt)


class InstallCommand(Command):
    """
    Install an extension.

    """
    name = 'install'
    help = 'Install an extension'

    arguments = [
        Argument(
            'name',
            help='The name of the extension'
        ),
        Argument(
            '--upgrade',
            action='store_true',
            default=False,
            help='Upgrade the extension to the latest version'
        )
    ]

    def execute(self, args: argparse.Namespace):
        available_extensions = get_available_extensions(args)
        if args.name not in available_extensions:
            raise Exception(
                '{} is not a valid extension name'.format(args.name))

        installer = get_installer(args)

        pip_cmd = [
            'pip', 'install',
            '--extra-index-url', get_python_package_repo(installer),
            '--trusted-host', installer
        ]

        if args.upgrade:
            pip_cmd.append('--upgrade')

        pip_cmd.append(args.name)

        subprocess.Popen(pip_cmd).wait()


class ExtensionsCommand(RootCommand):
    """
    Command for managing Tortuga CLI extensions.

    """
    name = 'extensions'
    help = 'Manage Tortuga CLI extensions'

    sub_commands = [
        ListCommand(),
        InstallCommand()
    ]

    arguments = [
        Argument(
            '--all',
            action='store_true',
            default=False
        )
    ]


def get_installer(args: argparse.Namespace) -> str:
    """
    Gets the hostname of the Tortuga installer.

    :param argparse.Namespace args: argparse arguments

    :return str: the URL

    """
    cm = ConfigManager()

    url, username, password, verify = get_web_service_config(args)
    if url:
        url_parts = url.split(':')
        host = url_parts[1].replace('//', '')

    else:
        host = cm.getInstaller()

    return host


def get_python_package_repo(installer: str) -> str:
    """
    Gets the URL to the Tortuga Python package repository.

    :param str installer: the hostname of the installer

    :return str: the URL

    """
    cm = ConfigManager()

    url = cm.getIntWebRootUrl(installer)

    return '{}/python-tortuga/simple/'.format(url)


def get_available_extensions(args: argparse.Namespace) -> List[str]:
    """
    Get a list of all available CLI extensions.

    :param argparse.Namespace args: argparse arguments

    :return List[str]: the list of available extensions

    """
    installer = get_installer(args)
    r = requests.get(get_python_package_repo(installer))
    if r.status_code != 200:
        raise Exception(
            'Repository returned status code: {}'.format(r.status_code)
        )

    tree = ElementTree()
    root = tree.parse(io.StringIO(r.text))

    extensions = []
    for e in root.findall('body/a'):
        name = e.text
        if args.all or 'cli' in name:
            extensions.append(name)

    return extensions
