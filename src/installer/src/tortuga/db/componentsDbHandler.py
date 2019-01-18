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

# pylint: disable=not-callable,multiple-statements,no-self-use,no-member

from sqlalchemy import and_, or_
from sqlalchemy.orm.exc import NoResultFound

from tortuga.db.tortugaDbObjectHandler import TortugaDbObjectHandler
from tortuga.exceptions.componentNotFound import ComponentNotFound
from tortuga.helper import osHelper
from .models.component import Component


class ComponentsDbHandler(TortugaDbObjectHandler):
    """
    This class handles components table.

    """

    def getComponentById(self, session, _id):
        """
        Raises:
            ComponentNotFound
        """

        dbComponent = session.query(Component).get(_id)

        if not dbComponent:
            raise ComponentNotFound('Component ID [%d] not found' % (_id))

        return dbComponent

    def getComponentByOsInfo(self, session, name, version, osInfo):
        """
        Raises:
            ComponentNotFound
        """

        try:
            return session.query(Component).filter(
                and_(Component.name == name,
                     Component.version == version,
                     Component.os.any(name=osInfo.getName(),
                                      version=osInfo.getVersion(),
                                      arch=osInfo.getArch()))
            ).one()
        except NoResultFound:
            raise ComponentNotFound(
                'Component [%s-%s] (%s) not found.' % (
                    name, version, osInfo))

    def getComponentByOsFamilyInfo(self, session, name, version,
                                   osFamilyInfo):
        try:
            return session.query(
                Component).filter(
                    and_(
                        Component.name == name,
                        Component.version == version,
                        Component.family.any(
                            name=osFamilyInfo.getName(),
                            version=osFamilyInfo.getVersion(),
                            arch=osFamilyInfo.getArch()))).one()
        except NoResultFound:
            raise ComponentNotFound(
                'Component [%s-%s] (%s) not found.' % (
                    name, version, osFamilyInfo))

    def getBestMatchComponent(self, session, name, version, osInfo, kitId):
        """
        Return best match component

        The query will search for an exact or family match.
        """

        self._logger.debug(
            'Retrieving best match component for %s-%s (%s)' % (
                name, version, osInfo))

        osConfig = osHelper.getOsInfo(
            osInfo.getName(), osInfo.getVersion(), osInfo.getArch())

        matchSpec = or_(
            Component.os.any(
                name=osInfo.getName(),
                version=osInfo.getVersion(),
                arch=osInfo.getArch()),
            Component.family.any(
                name=osConfig.getOsFamilyInfo().getName(),
                version=osConfig.getOsFamilyInfo().getVersion(),
                arch=osInfo.getArch()),
            Component.family.any(
                name=osConfig.getOsFamilyInfo().getName(),
                version=osConfig.getOsFamilyInfo().getVersion(),
                arch=None),
            Component.family.any(name='root')
        )

        if version:
            filter_spec = and_(Component.kitId == kitId,
                               Component.name == name,
                               Component.version == version, matchSpec)
        else:
            filter_spec = and_(Component.kitId == kitId,
                               Component.name == name, matchSpec)

        dbComponent = session.query(Component).filter(filter_spec).first()

        if not dbComponent:
            comp_label = '%s-%s' % (name, version) if version else name

            excmsg = 'Component %s (%s) is not found.' % (comp_label, osInfo)

            raise ComponentNotFound(excmsg)

        return dbComponent

    def getComponentList(self, session):
        """
        Get list of components from the db.
        """

        return session.query(Component).all()

    def getEnabledComponentList(self, session):
        """
        Get list of components from the db that are enabled.
        """

        return session.query(
            Component).filter(Component.softwareprofiles.any()).all()

    def getComponentFromComponentObject(self, session, component):
        for osInfo in component.getOsInfoList():
            self.getComponentByOsInfo(
                session, component.getName(), component.getVersion(),
                osInfo)

            break
        else:
            for osFamilyInfo in component.getOsFamilyInfoList():
                self.getComponentByOsFamilyInfo(
                    session, Component.name == component.getName(),
                    Component.version == component.getVersion(),
                    osFamilyInfo)
