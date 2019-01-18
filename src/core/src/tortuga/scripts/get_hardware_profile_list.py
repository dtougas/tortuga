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

from tortuga.cli.tortugaCli import TortugaCli
from tortuga.wsapi.hardwareProfileWsApi import HardwareProfileWsApi
from tortuga.cli.utils import FilterTagsAction


class GetHardwareProfileListCli(TortugaCli):
    def parseArgs(self, usage=None):
        self.addOption(
            '--tag',
            action=FilterTagsAction,
            dest='tags',
            help=_('Filter results by specified tag(s) (comma-separated)'),
        )

        super().parseArgs(usage=usage)

    def runCommand(self):
        self.parseArgs(_('Returns the list of hardware profiles in the'
                         ' system'))

        api = HardwareProfileWsApi(username=self.getUsername(),
                                   password=self.getPassword(),
                                   baseurl=self.getUrl(),
                                   verify=self._verify)

        for hp in api.getHardwareProfileList(tags=self.getArgs().tags):
            print(str(hp))


def main():
    GetHardwareProfileListCli().run()
