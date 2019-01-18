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

# pylint: disable=no-name-in-module,no-member
import logging
from typing import List

from tortuga.kit.registry import get_all_kit_installers
from tortuga.logging import KIT_NAMESPACE
from tortuga.objects.node import Node
from tortuga.objects.tortugaObjectManager import TortugaObjectManager


class KitActionsManager(TortugaObjectManager):
    def __init__(self):
        self._logger = logging.getLogger(KIT_NAMESPACE)
        
    def get_cloud_config(self, node, hardware_profile, software_profile,
                         user_data, *args, **kwargs):
        self._logger.debug(
            'get_cloud_config: {}, {}, {}, {}, {}'.format(
                node.name, hardware_profile.name, software_profile.name, args,
                kwargs
            )
        )

        for component_installer in self._get_enabled_component_installers(
                self._get_all_component_installers()):
            component_installer.run_action(
                'get_cloud_config',
                node,
                hardware_profile.name,
                software_profile.name,
                user_data,
                *args,
                **kwargs
            )

        return user_data

    def pre_add_host(
            self, hardware_profile_name: str, software_profile_name: str,
            hostname: str, ip: str) -> None:
        """
        This method is called from the resource adapter after a
        node/instance has been created but before control is returned back
        to add host workflow.
        """

        self._logger.debug(
            'pre_add_host: {}, {}, {}, {}'.format(
                hardware_profile_name, software_profile_name, hostname, ip
            )
        )

        for component_installer in self._get_enabled_component_installers(
                self._get_all_component_installers()):
            component_installer.run_action(
                'pre_add_host',
                hardware_profile_name,
                software_profile_name,
                hostname,
                ip
            )

    def post_add_host(
            self, hardware_profile_name: str, software_profile_name: str,
            nodes: List[Node]) -> None:
        """
        Post add host processing on the installer node.
        """

        self._logger.debug(
            'post_add_host: {}, {}, nodes={}'.format(
                hardware_profile_name, software_profile_name,
                '[...]' if nodes else '[]',
            )
        )

        self._run_action_with_node_list(
            self._get_enabled_component_installers(
                self._get_all_component_installers()),
            hardware_profile_name,
            software_profile_name,
            nodes,
            'add_host'
        )

    def refresh(self, software_profile_list, *args, **kwargs):
        self._logger.debug('refresh: {} {} kargs {}'.format(software_profile_list,
                                                      args, kwargs))

        component_installers = self._get_enabled_component_installers(
            self._get_all_component_installers())
        for component_installer in component_installers:
            component_installer.run_action(
                'refresh',
                software_profile_list,
                *args,
                **kwargs
            )

    def pre_delete_host(self, hardware_profile_name, software_profile_name,
                        *args, **kwargs):
        """
        Pre-delete host processing on installer node

        """
        self._delete_host_action(
            hardware_profile_name, software_profile_name, 'pre_delete_host',
            *args, **kwargs)

    def post_delete_host(self, hardware_profile_name, software_profile_name,
                         *args, **kwargs):
        """
        Post-delete host processing on installer node

        """
        self._delete_host_action(
            hardware_profile_name, software_profile_name, 'delete_host',
            *args, **kwargs)

    def _delete_host_action(self, hardware_profile_name,
                            software_profile_name, action_name,
                            *args, **kwargs):
        self._logger.debug(
            '{}: {}, {}, {}, {}'.format(
                action_name, hardware_profile_name, software_profile_name,
                args, kwargs
            )
        )

        component_installers = self._get_enabled_component_installers(
            self._get_all_component_installers(base_kit_order='last'))

        #
        # Get all nodes marked as 'Deleted' that may still exist in the
        # database. We shouldn't have to do this, but occasionally a
        # transient condition (ie. unable to connect to hypervisor) occurs
        # and the delete node operation fails.
        #
        from tortuga.db.nodesDbHandler import NodesDbHandler
        nodes_db = NodesDbHandler()

        if software_profile_name:
            nodes = nodes_db.getNodeListByNodeStateAndSoftwareProfileName(
                    self.session, 'Deleted', software_profile_name)
        else:
            nodes = nodes_db.getNodesByNodeState(self.session, 'Deleted')


        if 'nodes' in kwargs:
            aggregated_nodes = list(set(kwargs['nodes']) |
                                    set([node.name for node in nodes]))
            del kwargs['nodes']
        else:
            aggregated_nodes = nodes

        #
        # hardware profile currently undefined for delete_host() action,
        # so pass None as hardware profile name
        #
        self._run_action_with_node_list(component_installers,
                                        hardware_profile_name,
                                        software_profile_name,
                                        aggregated_nodes, action_name,
                                        *args, **kwargs)

    def _get_all_component_installers(self, base_kit_order='first'):
        all_components = []
        for kit_installer_class in self._load_kits(base_kit_order):
            kit_installer = kit_installer_class()
            kit_installer.session = self.session
            all_components.extend(
                kit_installer.get_all_component_installers())
        return all_components

    def _get_enabled_component_installers(self, component_list):
        from tortuga.db.softwareProfileDbApi import SoftwareProfileDbApi

        enabled_components = []
        api = SoftwareProfileDbApi()

        db_enabled_components = api.getAllEnabledComponentList(self.session)
        for component in component_list:
            for db_component in db_enabled_components:
                if component.name == db_component.getName():
                    enabled_components.append(component)
                    break
        return enabled_components

    def _run_action_with_node_list(self, component_installer_list,
                                   hardware_profile_name,
                                   software_profile_name, nodes, action_name,
                                   *args, **kwargs):
        for component_installer in component_installer_list:
            component_installer.run_action(
                action_name,
                hardware_profile_name,
                software_profile_name,
                nodes,
                *args,
                **kwargs
            )

    def _load_kits(self, base_kit_order='any'):
        """
        Return a list of all KitInstaller objects in the system

        """
        all_kit_installers = get_all_kit_installers()

        if base_kit_order in ['first', 'last']:
            base_kit_installer = None
            for kit in all_kit_installers:
                if kit.name == 'base':
                    base_kit_installer = kit
            if base_kit_installer:
                all_kit_installers.remove(base_kit_installer)
            if base_kit_order == 'first':
                all_kit_installers.insert(0, base_kit_installer)
            else:
                all_kit_installers.append(base_kit_installer)

        return all_kit_installers

    def load_component(self, component_name):
        """
        Return the ComponentInstaller object for the given component

        :param component_name:
        :return:

        """
        component_installers = self._get_all_component_installers()
        for component_installer in component_installers:
            if component_installer.name == component_name:
                return component_installer
        return None
