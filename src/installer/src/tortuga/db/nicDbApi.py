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

# pylint: disable=no-member

from tortuga.db.tortugaDbApi import TortugaDbApi

from sqlalchemy.orm.session import Session
from tortuga.db.nicsDbHandler import NicsDbHandler
from tortuga.exceptions.tortugaException import TortugaException


class NicDbApi(TortugaDbApi):
    """
    Nics DB API class
    """

    def __init__(self):
        TortugaDbApi.__init__(self)

        self._nicsDbHandler = NicsDbHandler()

    def setNicIp(self, session: Session, mac, ip):
        """
        Set NIC IP in database.
        """

        try:
            dbNics = self._nicsDbHandler.getNic(session, mac)

            self._logger.debug(
                'setNicIp: mac [%s] ip [%s]' % (mac, ip))

            dbNics.ip = ip
            session.commit()
            return
        except TortugaException:
            session.rollback()
            raise
        except Exception as ex:
            session.rollback()
            self._logger.exception(str(ex))
            raise

    def setIp(self, session: Session, nicId, ip):
        try:
            dbNic = self._nicsDbHandler.getNicById(session, nicId)

            self._logger.debug('setIp: nicId [%s] ip [%s]' % (
                nicId, ip))

            dbNic.ip = ip

            session.commit()

            return
        except TortugaException:
            session.rollback()
            raise
        except Exception as ex:
            session.rollback()
            self._logger.exception(str(ex))
            raise
