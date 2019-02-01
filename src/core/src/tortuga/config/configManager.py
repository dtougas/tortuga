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

import configparser
import os
import shlex
import socket
from typing import Optional, Union

from tortuga.objects.provisioningInfo import ProvisioningInfo
from tortuga.utility.helper import str2bool


# Defaults.
DEFAULT_TORTUGA_ROOT = '/opt/tortuga'
DEFAULT_TORTUGA_CA_BUNDLE = '/etc/pki/tls/certs/ca-bundle.crt'
DEFAULT_TORTUGA_ETC = os.path.join(DEFAULT_TORTUGA_ROOT, 'etc')
DEFAULT_TORTUGA_BIN = os.path.join(DEFAULT_TORTUGA_ROOT, 'bin')
DEFAULT_TORTUGA_CONFIG_BASE = os.path.join(DEFAULT_TORTUGA_ROOT, 'config')

DEFAULT_TORTUGA_REPO_CONFIG_FILE = os.path.join(
    DEFAULT_TORTUGA_CONFIG_BASE, 'repo.conf')
DEFAULT_TORTUGA_ADMIN_PORT = 8443
DEFAULT_TORTUGA_WEBSOCKET_PORT = 9443
DEFAULT_TORTUGA_WEBSOCKET_SCHEME = 'wss'
DEFAULT_TORTUGA_INT_WEBSERVICE_PORT = 8444
DEFAULT_TORTUGA_ADMIN_SCHEME = 'https'
DEFAULT_TORTUGA_INT_WEB_SCHEME = 'http'
DEFAULT_TORTUGA_INT_WEB_PORT = 8008
DEFAULT_TORTUGA_DNS_ZONE = 'localdomain'
DEFAULT_TORTUGA_TIME_ZONE = 'GMT'
DEFAULT_TORTUGA_DB_PASSWORD = ''
DEFAULT_TORTUGA_DB_PASSWORD_FILE = os.path.join(
    DEFAULT_TORTUGA_ETC, 'db.passwd')
DEFAULT_TORTUGA_REDIS_PASSWORD = ''
DEFAULT_TORTUGA_REDIS_PASSWORD_FILE = os.path.join(
    DEFAULT_TORTUGA_ETC, 'redis.passwd')
DEFAULT_TORTUGA_DB_USER = 'apache'
DEFAULT_TORTUGA_DB_SCHEMA = 'tortugadb'
DEFAULT_TORTUGA_CFM_ROOT_DIR = '/etc/cfm'
DEFAULT_TORTUGA_CFM_SECRET_FILE = os.path.join(
    DEFAULT_TORTUGA_CFM_ROOT_DIR, '.cfmsecret')
DEFAULT_TORTUGA_CFM_USER = "cfm"
DEFAULT_TORTUGA_CFM_PASSWORD = "not-set"
DEFAULT_TORTUGA_RELEASE = 'development'
DEFAULT_TORTUGA_WEB_ROOT = '/tortuga'
DEFAULT_TORTUGA_KIT_DIR = 'kits'
DEFAULT_TORTUGA_DEPOT_DIR = DEFAULT_TORTUGA_ROOT + '/depot'
DEFAULT_TORTUGA_RULES_SUBDIRECTORY = 'var/rules'
DEFAULT_TORTUGA_RULES_DIR = os.path.join(DEFAULT_TORTUGA_ROOT,
                                         DEFAULT_TORTUGA_RULES_SUBDIRECTORY)
DEFAULT_TORTUGA_WWW_PUBLIC = 'www'
DEFAULT_TORTUGA_WWW_INTERNAL = 'www_int'
DEFAULT_TORTUGA_RELATIVE_REPOS_DIR = os.path.join(
    DEFAULT_TORTUGA_WWW_INTERNAL, 'repos')
DEFAULT_TORTUGA_RELATIVE_KICKSTARTS_DIR = os.path.join(
    DEFAULT_TORTUGA_WWW_INTERNAL, 'kickstarts')
DEFAULT_TORTUGA_ACTION_LOG = '/var/action-log'

DEFAULT_TORTUGA_PROFILE_NII_FILE = '/etc/profile.nii'
DEFAULT_TORTUGA_RELEASE_FILE = os.path.join(
    DEFAULT_TORTUGA_ETC, 'tortuga-release')

DEFAULT_PROVISIONING_INFO = None

# The most amount of data we will read when parsing provisioning info object
MAX_PROVINFO_LENGTH = 50000


def get_default_dns_suffix() -> Union[str, None]:
    if not os.path.exists('/etc/resolv.conf'):
        return None

    domain_name = None
    search_domain_name = None

    with open('/etc/resolv.conf') as fp:
        for buf in fp.readlines():
            if search_domain_name is None and buf.startswith('search'):
                result = shlex.split(buf.rstrip())
                if len(result) < 2:
                    continue

                # use first entry after "search ..."
                search_domain_name = result[1].lower()
            elif buf.startswith('domain'):
                result = shlex.split(buf.rstrip())
                if len(result) < 2:
                    continue

                # use argument to "domain ..."
                domain_name = result[1].lower()

    if domain_name:
        return domain_name

    return search_domain_name


def getfqdn():
    fqdn = socket.getfqdn()
    if '.' in fqdn:
        return fqdn

    default_dns_suffix = get_default_dns_suffix()
    if default_dns_suffix:
        return f'{fqdn}.{default_dns_suffix}'

    return fqdn


def lookup_ipaddress(fqdn: str) -> str:
    aiInfo = socket.getaddrinfo(fqdn, None, socket.AF_INET, socket.SOCK_STREAM)

    return aiInfo[0][4][0]


class ConfigManager(dict): \
        # pylint: disable=too-many-public-methods
    """
    Class used for keeping system configuration data. The class
    initializes its data using predefined defaults, or from the following
    environment variables:
        TORTUGA_ROOT
        TORTUGA_REPO_CONFIG_FILE

    Usage:
        from tortuga.config.configManager import ConfigManager
        cm = ConfigManager()
        cm.setConsoleLogLevel('info')
        level = cm.getConsoleLogLevel()
        cm['myKey'] = 'myValue'
        value = cm.get('myKey')
    """
    def __init_defaults(self):
        self['defaultRoot'] = DEFAULT_TORTUGA_ROOT
        self['defaultCaBundle'] = DEFAULT_TORTUGA_CA_BUNDLE
        self['defaultRepoConfigFile'] = DEFAULT_TORTUGA_REPO_CONFIG_FILE
        self['defaultDnsZone'] = DEFAULT_TORTUGA_DNS_ZONE
        self['defaultTimeZone'] = DEFAULT_TORTUGA_TIME_ZONE
        self['defaultAdminPort'] = DEFAULT_TORTUGA_ADMIN_PORT
        self['defaultIntWebservicePort'] = \
            DEFAULT_TORTUGA_INT_WEBSERVICE_PORT
        self['defaultWebsocketScheme'] = DEFAULT_TORTUGA_WEBSOCKET_SCHEME
        self['defaultWebsocketPort'] = DEFAULT_TORTUGA_WEBSOCKET_PORT
        self['defaultAdminScheme'] = DEFAULT_TORTUGA_ADMIN_SCHEME
        self['defaultIntWebScheme'] = DEFAULT_TORTUGA_INT_WEB_SCHEME
        self['defaultIntWebPort'] = DEFAULT_TORTUGA_INT_WEB_PORT
        self['defaultDbPassword'] = DEFAULT_TORTUGA_DB_PASSWORD
        self['defaultDbPasswordFile'] = DEFAULT_TORTUGA_DB_PASSWORD_FILE
        self['defaultRedisPassword'] = DEFAULT_TORTUGA_REDIS_PASSWORD
        self['defaultRedisPasswordFile'] = DEFAULT_TORTUGA_REDIS_PASSWORD_FILE
        self['defaultDbUser'] = DEFAULT_TORTUGA_DB_USER
        self['defaultDbSchema'] = DEFAULT_TORTUGA_DB_SCHEMA
        self['defaultCfmSecretFile'] = DEFAULT_TORTUGA_CFM_SECRET_FILE
        self['defaultCfmUser'] = DEFAULT_TORTUGA_CFM_USER
        self['defaultCfmPassword'] = DEFAULT_TORTUGA_CFM_PASSWORD
        self['defaultTortugaRelease'] = DEFAULT_TORTUGA_RELEASE
        self['defaultTortugaWebRoot'] = DEFAULT_TORTUGA_WEB_ROOT
        self['defaultTortugaKitDir'] = DEFAULT_TORTUGA_KIT_DIR
        self['defaultTortugaDepotDir'] = DEFAULT_TORTUGA_DEPOT_DIR
        self['defaultTortugaRulesDir'] = DEFAULT_TORTUGA_RULES_DIR
        self['defaultProfileNiiFile'] = DEFAULT_TORTUGA_PROFILE_NII_FILE
        self['defaultProvisioningInfo'] = DEFAULT_PROVISIONING_INFO
        self['defaultKitConfigBase'] = DEFAULT_TORTUGA_CONFIG_BASE
        self['defaultActionLog'] = DEFAULT_TORTUGA_ACTION_LOG

    def __init_from_env(self):
        # Settings that might come from environment variables.
        self.__setFromEnvVariable('root', 'TORTUGA_ROOT')
        self.__setFromEnvVariable(
            'repoConfigFile', 'TORTUGA_REPO_CONFIG_FILE')

    def __init_from_provinfo(self):
        # Initialize the ProvisioningInfo structure
        self.__initializeProvisioningInfo(DEFAULT_TORTUGA_PROFILE_NII_FILE)

        # Other settings.
        self.__setFromProvisioningInfo('installer', 'Installer')
        self.__setFromProvisioningInfo('dnsZone', 'DNSZone')
        self.__setFromProvisioningInfo('timeZone', 'Timezone_zone')
        self.__setFromProvisioningInfo('intWebPort', 'IntWebPort')
        if self.get('intWebPort'):
            self['intWebPort'] = int(self['intWebPort'])

        self.__setFromProvisioningInfo(
            'intWebservicePort', 'IntWebServicePort')

        if self.get('intWebservicePort'):
            self['intWebservicePort'] = int(self['intWebservicePort'])

        self.__setFromProvisioningInfo('adminPort', 'WebservicePort')

    def __init_from_varfile(self):
        self.__setFromVarFile(
            'dbPassword', DEFAULT_TORTUGA_DB_PASSWORD_FILE)

        self.__setFromVarFile(
            'redisPassword', DEFAULT_TORTUGA_REDIS_PASSWORD_FILE)

        self.__setFromVarFile(
            'tortugaRelease', DEFAULT_TORTUGA_RELEASE_FILE)

        self.__setFromVarFile(
            'cfmPassword', DEFAULT_TORTUGA_CFM_SECRET_FILE)

    def __init__(self):
        super(ConfigManager, self).__init__()

        self.__init_defaults()

        self.__init_from_env()

        # Variables affected by TORTUGA_ROOT
        self.__setRootSubdirectories()

        self.__init_from_provinfo()

        # Normalize 'adminPort'
        if self.get('adminPort'):
            self['adminPort'] = int(self['adminPort'])

        self.__init_from_varfile()

        # Set host based on provisioning info
        if self.getProvisioningInfo() is None:
            self['installer'] = self['host'] = getfqdn()
        else:
            self['host'] = self.getProvisioningInfo().getNode().getName()

    def __setRootSubdirectories(self):
        etc_dir = os.path.join(self.getRoot(), 'etc')
        cfg_dir = os.path.join(self.getRoot(), 'config')

        self['reposDir'] = os.path.join(
            self.getRoot(), DEFAULT_TORTUGA_RELATIVE_REPOS_DIR)
        self['tortugaDepotDir'] = os.path.join(self.getRoot(), 'depot')
        self['kickstartsDir'] = os.path.join(
            self.getRoot(), DEFAULT_TORTUGA_RELATIVE_KICKSTARTS_DIR)
        self['webRoot'] = os.path.join(
            self.getRoot(), DEFAULT_TORTUGA_WWW_PUBLIC)
        self['intWebRoot'] = os.path.join(
            self.getRoot(), DEFAULT_TORTUGA_WWW_INTERNAL)
        self['binDir'] = os.path.join(self.getRoot(), 'bin')
        self['etcDir'] = etc_dir
        self['kitConfigBase'] = cfg_dir
        self['logConfigFile'] = os.path.join(cfg_dir, 'log.conf')

        self['tortugaRulesDir'] = os.path.join(
            self.getRoot(), DEFAULT_TORTUGA_RULES_SUBDIRECTORY)

        self['dbPasswordFile'] = os.path.join(etc_dir, 'db.passwd')
        self['redisPasswordFile'] = os.path.join(etc_dir, 'redis.passwd')

        self['inifile'] = os.path.join(cfg_dir, 'tortuga.ini')

    def __initializeProvisioningInfo(self, envFile):
        if not os.path.exists(envFile):
            return

        with open(envFile) as f:
            xmlstring = f.read(MAX_PROVINFO_LENGTH)

        if not xmlstring:
            return

        self['defaultProvisioningInfo'] = \
            ProvisioningInfo.getFromXml(xmlstring)

    def __setFromEnvVariable(self, key, envVar):
        """
        Set value for the specified key from a given environment variable.
        This functions ignores errors for env. variables that are not set.
        """

        if envVar in os.environ:
            self[key] = os.environ[envVar]

    # This function will return None for variables that are not accessible
    def __setFromProvisioningInfo(self, key, varKey):
        """
        Set value for the specified key from a given environment file.
        """
        if self.getProvisioningInfo() is not None:
            self[key] = self.getProvisioningGlobalParameter(varKey)

    # This function will ignore errors if variable file is not present.
    def __setFromVarFile(self, key, varFile):
        """
        Set value for the specified key from a given file. The first line
        in the file is variable value.
        This functions ignores errors.
        """

        if os.path.exists(varFile):
            try:
                with open(varFile) as v:
                    self[key] = v.readline().lstrip().rstrip()
            except IOError as exc:
                # Ignore 'Permission denied', raise all others
                if exc.errno != 13:
                    raise

    def __getKeyValue(self, key, default='__internal__'):
        """
        Get value for a given key.
        Keys will be of the form 'logFile', and the default keys have
        the form 'defaultLogFile'.
        """
        defaultKey = "default" + key[0].upper() + key[1:]
        defaultValue = self.get(defaultKey, None)
        if default != '__internal__':
            defaultValue = default
        return self.get(key, defaultValue)

    def getHost(self):
        """ Get machine hostname. """
        return self['host']

    def getIpAddress(self):
        return lookup_ipaddress(self.getHost())

    def setRoot(self, root):
        """ Set root. """
        self['root'] = root

        self.__setRootSubdirectories()

    def getRoot(self, default='__internal__'):
        """
        Get tortuga root. If the root has not been set, the function
        will return the specified default value. If the default value is
        not specified, internal (predefined) default will be returned.
        """
        return self.__getKeyValue('root', default)

    def setCaBundle(self, path: str):
        """
        Set the path to the SSL CA bundle.

        """
        self['caBundle'] = path

    def getCaBundle(self, default: str = '__internal__') -> str:
        """
        Get the path to the SSL CA bundle.

        """
        return self.__getKeyValue('caBundle', default)

    def getBinDir(self, default='__internal__'):
        return self.__getKeyValue('binDir', default)

    def getEtcDir(self, default='__internal__'):
        return self.__getKeyValue('etcDir', default)

    def getLogFile(self, default='__internal__'):
        """
        Get log file. If the log file has not been set, the function
        will return the specified default value. If the default value is
        not specified, internal (predefined) default will be returned.
        """
        return self.__getKeyValue('logFile', default)

    def getLogConfigFile(self, default='__internal__'):
        """
        Get logging configuration file. If the configuration file has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('logConfigFile', default)

    def setConsoleLogLevel(self, level):
        """ Set user log level. """
        self['consoleLogLevel'] = level

    def getConsoleLogLevel(self, default='__internal__'):
        """
        Get user log level. If the user log level has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('consoleLogLevel', default)

    def setFileLogLevel(self, level):
        """ Set system log level. """
        self['fileLogLevel'] = level

    def getFileLogLevel(self, default='__internal__'):
        """
        Get system log level. If the system log level has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('fileLogLevel', default)

    def setLogRecordFormat(self, format_):
        """ Set log record format. """
        self['logRecordFormat'] = format_

    def getLogRecordFormat(self, default='__internal__'):
        """
        Get log record format. If the log record format has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('logRecordFormat', default)

    def getLogDateFormat(self, default='__internal__'):
        """
        Get log date (timestamp) format. If the log date format has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('logDateFormat', default)

    def setRepoConfigFile(self, repoConfigFile):
        """ Set repo configuration file. """
        self['repoConfigFile'] = repoConfigFile

    def getRepoConfigFile(self, default='__internal__'):
        """
        Get repo configuration file. If the configuration file has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('repoConfigFile', default)

    def setInstaller(self, installer):
        """ Set installer. """
        self['installer'] = installer

    def getInstaller(self, default='__internal__'):
        """
        Get installer. If installer has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('installer', default)

    def isInstaller(self):
        ''' Returns True if this node is the Installer Node '''
        if self.getProvisioningInfo() is None:
            # This is to make sure it works when a profile.nii is not there
            return True

        # Now check with valid profile.nii
        installer = self.getInstaller(default=None)
        if installer is not None and installer == self.getHost():
            return True
        return False

    def getInstallerUrl(self, hostname=None, path=None):
        '''
        Get the URL of the Primary Install Node,
        with an optional path, if given.
        '''

        hostname = hostname if hostname else self.getInstaller()

        url = '%s://%s:%s' % (self.getAdminScheme(),
                              hostname,
                              self.getAdminPort())

        if path is not None and path != '':
            if not path.startswith('/'):
                url += '/'
            url += path

        return url

    def getIntWebScheme(self, default='__internal__'):
        """Return scheme for internal web server."""
        return self.__getKeyValue('intWebScheme', default)

    def setAdminScheme(self, adminScheme):
        """ Set admin scheme. """
        self['adminScheme'] = adminScheme

    def getAdminScheme(self, default='__internal__'):
        """
        Get the admin scheme
        """
        return self.__getKeyValue('adminScheme', default)

    def setWebsocketScheme(self, websocketScheme: str):
        """
        Set the websocket scheme.

        :param str websocketScheme: the websocket scheme (ws or wss...)

        """
        self['websocketScheme'] = websocketScheme

    def getWebsocketScheme(self, default: str = '__internal__') -> str:
        """
        Get the websocket scheme (ws, or wss...)

        """
        return self.__getKeyValue('websocketScheme', default)

    def setWebsocketPort(self, websocketPort: int):
        """
        Set the websocket port.

        :param str websocketPort: the websocket port

        """
        self['websocketPort'] = websocketPort

    def getWebsocketPort(self, default: str = '__internal__') ->int:
        """
        Get the websocket port

        """
        return self.__getKeyValue('websocketPort', default)

    def setIntWebServicePort(self, intWebservicePort):
        """ Set internal webservice port. """
        self['intWebservicePort'] = intWebservicePort

    def getIntWebServicePort(self, default='__internal__'):
        """
        Get internal webservice port.
        """
        return int(self.__getKeyValue('intWebservicePort', default))

    def setAdminPort(self, adminPort):
        """ Set admin port. """
        self['adminPort'] = adminPort

    def getAdminPort(self, default='__internal__'):
        """
        Get admin port. If admin port has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return int(self.__getKeyValue('adminPort', default))

    def setKitConfigBase(self, kitConfigBase):
        """ Set kit configuration base directory. """
        self['kitConfigBase'] = kitConfigBase

    def getKitConfigBase(self, default='__internal__'):
        """
        Get kit configuration base directory. If kit configuration base
        directory has not been set, the function will return the
        specified default value.

        If the default value is not specified, internal (predefined)
        default will be returned.
        """

        return self.__getKeyValue('kitConfigBase', default)

    def getDbPassword(self, default='__internal__'):
        """
        Get db password. If db password has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('dbPassword', default)

    def getRedisPassword(self, default='__internal__'):
        """
        Get Redis password. If Redis password has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.

        """
        return self.__getKeyValue('redisPassword', default)

    def getCfmSecretFile(self, default='__internal__'):
        """ return cfm root dir...use default if not defined """
        return self.__getKeyValue('cfmSecretFile', default)

    def setCfmSecretFile(self, filepath):
        self['cfmSecretFile'] = filepath

    def getCfmUser(self, default='__internal__'):
        """ return cfm user name """
        return self.__getKeyValue('cfmUser', default)

    def getCfmPassword(self, default='__internal__'):
        """ return cfm user password """
        return self.__getKeyValue('cfmPassword', default)

    def getProfileNiiFile(self, default='__internal__'):
        return self.__getKeyValue('profileNiiFile', default)

    def getWebRoot(self, default='__internal__'):
        """ return root dir...use default if not defined """
        return self.__getKeyValue('tortugaWebRoot', default)

    def getKitDir(self, default='__internal__'):
        """ return root dir...use default if not defined """
        kit_dir = self.__getKeyValue('tortugaKitDir', default)
        if os.path.isabs(kit_dir):
            return kit_dir
        return os.path.join(self.getRoot(default), kit_dir)

    def getTortugaRelease(self, default='__internal__'):
        """
        Get tortuga release. If release has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('tortugaRelease', default)

    def getDnsZone(self, default='__internal__'):
        """
        Get dns zone. If dns zone has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('dnsZone', default)

    def getTimeZone(self, default='__internal__'):
        """
        Get time zone. If time zone has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('timeZone', default)

    def getDbPasswordFile(self, default='__internal__'):
        """ return db password file...use default if not defined """
        return self.__getKeyValue('dbPasswordFile', default)

    def getRedisPasswordFile(self, default='__internal__'):
        """
        Return Redis password file, or use default if not defined.

        """
        return self.__getKeyValue('redisPasswordFile', default)

    def getDbUser(self, default='__internal__'):
        """ return db user ...use default if not defined """
        return self.__getKeyValue('dbUser', default)

    def getDbSchema(self, default='__internal__'):
        """ return db schema ...use default if not defined """
        return self.__getKeyValue('dbSchema', default)

    def getDepotDir(self, default='__internal__'):
        """ return depot dir...use default if not defined """
        return self.__getKeyValue('tortugaDepotDir', default)

    def setDepotDir(self, d):
        """ Set the depot dir """
        self['tortugaDepotDir'] = d

    def getRulesDir(self, default='__internal__'):
        """ return rules dir...use default if not defined """
        return self.__getKeyValue('tortugaRulesDir', default)

    def getProvisioningInfo(self, default='__internal__'):
        """
        Get the provisioning info object for this node...if the
        value has not been set the default will be returned.
        """
        return self.__getKeyValue('provisioningInfo', default)

    def getActionLog(self, default='__internal__'):
        """
        Get action log file. If action log file has not
        been set, the function will return the specified default value.
        If the default value is not specified, internal (predefined)
        default will be returned.
        """
        return self.__getKeyValue('actionLog', default)

    def getProvisioningGlobalParameter(self, name):
        pInfo = self.getProvisioningInfo()
        if pInfo is not None:
            for param in pInfo.getGlobalParameters():
                if param.getName() == name:
                    return param.getValue()
        return None

    def getReposDir(self, default='__internal__'):
        return self.__getKeyValue('reposDir', default)

    def getKickstartsDir(self, default='__internal__'):
        return self.__getKeyValue('kickstartsDir', default)

    def getTortugaWebRoot(self, default='__internal__'):
        return self.__getKeyValue('webRoot', default)

    def getTortugaIntWebRoot(self, default='__internal__'):
        return self.__getKeyValue('intWebRoot', default)

    def setIntWebPort(self, port):
        self['intWebPort'] = int(port)

    def getIntWebPort(self, default='__internal__'):
        return int(self.__getKeyValue('intWebPort', default))

    def getIntWebRootUrl(self, host: Optional[str] = None):
        installer_fqdn = host if host is not None else self.getInstaller()

        return '{}://{}:{}'.format(
            self.getIntWebScheme(), installer_fqdn, self.getIntWebPort()
        )

    def getYumRoot(self):
        return os.path.join(self.getTortugaIntWebRoot(), 'repos')

    def getYumRootUrl(self, host):
        return os.path.join(self.getIntWebRootUrl(host), 'repos')

    def getYumKit(self, name, vers, arch):
        return '%s/%s/%s/%s' % (self.getYumRoot(), name, vers, arch)

    def getYumKitUrl(self, host, name, vers, arch):
        return '%s/%s/%s/%s' % (self.getYumRootUrl(host), name, vers, arch)

    def getIniFile(self):
        return self['inifile']

    def _get_cfg(self):
        cfg = configparser.ConfigParser()
        cfg.read(self.getIniFile())

        return cfg

    def get_database_engine(self) -> str:
        cfg = self._get_cfg()

        if not cfg.has_option('database', 'engine'):
            return 'sqlite'

        return cfg.get('database', 'engine')

    def is_offline_installation(self) -> bool:
        cfg = self._get_cfg()

        if not cfg.has_option('installer', 'offline_installation'):
            return False

        return str2bool(cfg.get('installer', 'offline_installation'))
