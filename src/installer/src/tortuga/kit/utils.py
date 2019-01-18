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

import filecmp
import json
import logging
import os
import os.path
import shutil
import subprocess
import urllib.error
import urllib.request

from tortuga.config.configManager import ConfigManager
from tortuga.exceptions.fileNotFound import FileNotFound
from tortuga.exceptions.tortugaException import TortugaException
from tortuga.kit.metadata import KitMetadataSchema
from tortuga.logging import KIT_NAMESPACE
from tortuga.os_utility.tortugaSubprocess import TortugaSubprocess

logger = logging.getLogger(KIT_NAMESPACE)


def pip_install_requirements(requirements_path):
    """
    Installs packages specified in a requirements.txt file, using the tortuga
    package repo in addition to the standard python repos. This function
    returns nothing, and does nothing if the requirements.txt file is not
    found.

    :param requirements_path: the path to the requirements.txt file

    """
    cm = ConfigManager()

    if not os.path.exists(requirements_path):
        logger.debug('Requirements not found: {}'.format(requirements_path))
        return

    if is_requirements_empty(requirements_path):
        logger.debug('Requirements empty: {}'.format(requirements_path))
        return

    pip_cmd = [
        '{}/pip'.format(cm.getBinDir()),
        'install',
    ]

    installer = cm.getInstaller()
    int_webroot = cm.getIntWebRootUrl(installer)
    installer_repo = '{}/python-tortuga/simple/'.format(int_webroot)

    if cm.is_offline_installation():
        # add tortuga distribution repo
        pip_cmd.append('--index-url')
        pip_cmd.append(installer_repo)

        # add offline dependencies repo
        pip_cmd.append('--extra-index-url')
        pip_cmd.append('{}/offline-deps/python/simple/'.format(int_webroot))
    else:
        pip_cmd.append('--extra-index-url')

        pip_cmd.append(installer_repo)

    pip_cmd.extend([
        '--trusted-host', installer,
        '-r', requirements_path
    ])

    logger.debug(' '.join(pip_cmd))
    proc = subprocess.Popen(pip_cmd)
    proc.wait()
    if proc.returncode:
        raise Exception(proc.stderr)


def is_requirements_empty(requirements_file_path):
    """
    Tests to see if a pip requirements.txt file is empty.

    :param requirements_file_path: the path to the requirements.txt file
    :return:                       True if it is empty, False otherwise

    """
    fp = open(requirements_file_path)
    line_count = 0
    for line in fp.readline():
        line = line.strip()
        #
        # Skip blank lines, or comment lines
        #
        if not line or line.startswith('#'):
            continue
        line_count += 1
    return line_count == 0


def assembleKitUrl(srcUrl, kitFileName):
    """
    Construct kit url.

    """
    if os.path.basename(srcUrl) != kitFileName:
        return '%s/%s' % (srcUrl, kitFileName)

    return srcUrl


def copy(srcFile, destDir):
    """
    :raises FileNotFound:

    """

    destFile = '%s/%s' % (destDir, os.path.basename(srcFile))

    if os.path.exists(destFile) and filecmp.cmp(srcFile, destFile):
        logger.debug('Files [%s] and [%s] are the same, skipping copy.' % (
            srcFile, destFile))
    else:
        logger.debug('Copying [%s] to [%s]' % (srcFile, destFile))

        try:
            shutil.copy(srcFile, destDir)
        except Exception as ex:
            logger.debug('Copy failed, exception reported: %s' % ex)

            raise FileNotFound('Invalid kit at [%s]' % (srcFile))


def checkSupportedScheme(srcUrl):
    return srcUrl.startswith('http://') or srcUrl.startswith('https://') \
           or srcUrl.startswith('file://') or srcUrl.startswith('ftp://')


def retrieve(kitFileName, srcUrl, destDir):
    """
    :raises FileNotFound:

    """
    if checkSupportedScheme(srcUrl):
        # This is a urllib2 supported url scheme, download kit.
        kitUrl = assembleKitUrl(srcUrl, kitFileName)
        download([kitUrl], destDir)
    elif os.path.isdir(srcUrl):
        kitUrl = assembleKitUrl(srcUrl, kitFileName)
        copy(kitUrl, destDir)
    elif os.path.isfile(srcUrl) and \
            os.path.basename(srcUrl) == kitFileName:
        copy(srcUrl, destDir)
    else:
        raise FileNotFound(
            'File [%s] not found at URL [%s]' % (kitFileName, srcUrl))

    return assembleKitUrl(destDir, kitFileName)


def download(urlList, dest):
    """
    TODO: this should use a curl/wget download module

    """
    for url in urlList:
        i = url.rfind('/')

        destFile = dest + '/' + url[i + 1:]

        logger.debug(url + '->' + destFile)

        try:
            filein = urllib.request.urlopen(url)
        except urllib.error.URLError as ex:
            if ex.code == 404:
                raise FileNotFound('File not found at URL [%s]' % (url))

            raise TortugaException(exception=ex)
        except Exception as ex:
            raise TortugaException(exception=ex)

        fileout = open(destFile, "wb")

        while True:
            try:
                buf = filein.read(1024000)

                fileout.write(buf)
            except IOError as ex:
                raise TortugaException(exception=ex)

            if not bytes:
                break

        filein.close()
        fileout.close()
        logger.debug('Successfully dowloaded file [%s]' % (destFile))


def get_metadata_from_archive(kit_archive_path: str) -> dict:
    """
    Extracts and validates kit metadata from a kit archive file.

    :param str kit_archive_path: the path to the kit archive

    :return dict: the validated kit metadata

    """
    cmd = 'tar -xjOf {} \*/kit.json'.format(kit_archive_path)
    p = TortugaSubprocess(cmd)
    p.run()

    try:
        meta_dict: dict = json.loads(p.getStdOut().decode())
        errors = KitMetadataSchema().validate(meta_dict)
        if errors:
            raise TortugaException(
                'Incomplete kit metadata: {}'.format(meta_dict)
            )

    except json.JSONDecodeError:
        raise Exception('Invalid JSON for kit metadata: {}'.format(p.stdout))

    return meta_dict


def unpack_kit_archive(kit_archive_path: str, dest_root_dir: str) -> str:
    """
    Unpacks a kit archive into a directory.

    :param str kit_archive_path: the path to the kit archive
    :param str dest_root_dir:    the destination directory in which the
                                 archive will be extracted

    :return the kit installation directory

    """
    meta_dict = get_metadata_from_archive(kit_archive_path)

    destdir = os.path.join(
        dest_root_dir,
        'kit-{}'.format(
            format_kit_descriptor(meta_dict['name'],
                                  meta_dict['version'],
                                  meta_dict['iteration'])
        )
    )

    if not os.path.exists(destdir):
        os.mkdir(destdir)

    logger.debug(
        '[utils.parse()] Unpacking [%s] into [%s]' % (
            kit_archive_path, destdir))

    #
    # Extract the file
    #
    cmd = 'tar --extract --bzip2 --strip-components 1 --file {} -C {}'.format(
        kit_archive_path, destdir)
    TortugaSubprocess(cmd).run()

    #
    # Remove world write permissions, if any
    #
    cmd = 'chmod -R a-w {}'.format(destdir)
    TortugaSubprocess(cmd).run()

    logger.debug(
        '[utils.parse()] Unpacked [%s] into [%s]' % (
            kit_archive_path, destdir))

    return destdir


def format_kit_descriptor(name, version, iteration):
    """
    Returns a properly formatted kit 'descriptor' string in the format
    <name>-<version>-<iteration>

    """
    return '{0}-{1}-{2}'.format(name, version, iteration)


def format_component_descriptor(name, version):
    """
    Return a properly formatted component 'descriptor' in the format
    <name>-<version>

    """
    return '{0}-{1}'.format(name, version)
