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

"""
Helper script for retrieving a YAML hash of provisioning networks.
Used by Puppet

"""

import yaml

from tortuga.cli.tortugaCli import TortugaCli
from tortuga.wsapi.networkWsApi import NetworkWsApi


class GetProvisioningNetworks(TortugaCli):
    def runCommand(self):
        self.parseArgs(_('Returns a YAML list of provisioning networks'))

        api = NetworkWsApi(username=self.getUsername(),
                           password=self.getPassword(),
                           baseurl=self.getUrl(),
                           verify=self._verify)

        data = []
        for network in api.getNetworkList():
            if network.isProvisioning():
                data.append({'network': network.getAddress(),
                             'netmask': network.getNetmask()})

        print(yaml.safe_dump(data))


def main():
    GetProvisioningNetworks().run()
