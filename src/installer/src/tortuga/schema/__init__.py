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

# pylint: disable=too-few-public-methods

from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema
from tortuga.db.models.node import Node as NodeModel
from tortuga.db.models.softwareProfile \
    import SoftwareProfile as SoftwareProfileModel
from tortuga.db.models.hardwareProfile \
    import HardwareProfile as HardwareProfileModel
from tortuga.db.models.component import Component as ComponentModel
from tortuga.db.models.kit import Kit as KitModel
from tortuga.db.models.nic import Nic as NicModel
from tortuga.db.models.network import Network as NetworkModel
from tortuga.db.models.operatingSystem \
    import OperatingSystem as OperatingSystemModel
from tortuga.db.models.operatingSystemFamily \
    import OperatingSystemFamily as OperatingSystemFamilyModel
from tortuga.db.models.osComponent import OsComponent as OsComponentModel
from tortuga.db.models.osFamilyComponent \
    import OsFamilyComponent as OsFamilyComponentModel
from tortuga.db.models.resourceAdapter \
    import ResourceAdapter as ResourceAdapterModel
from tortuga.db.models.networkDevice import NetworkDevice as NetworkDeviceModel


class OperatingSystemSchema(ModelSchema):
    family = fields.Nested('OperatingSystemFamilySchema', exclude=('children',))

    class Meta:
        model = OperatingSystemModel


class OperatingSystemFamilySchema(ModelSchema):
    class Meta:
        model = OperatingSystemFamilyModel


class NetworkDeviceSchema(ModelSchema):
    class Meta:
        model = NetworkDeviceModel


class NicSchema(ModelSchema):
    networkdevice = fields.Nested('NetworkDeviceSchema')

    class Meta:
        model = NicModel


class NetworkSchema(ModelSchema):
    nics = fields.Nested('NicSchema', many=True, exclude=('networks',))

    class Meta:
        model = NetworkModel


class KitSchema(ModelSchema):
    class Meta:
        model = KitModel


class OsComponentSchema(ModelSchema):
    os = fields.Nested('OperatingSystem')
    class Meta:
        model = OsComponentModel


class OsFamilyComponentSchema(ModelSchema):
    family = fields.Nested('OperatingSystemFamilySchema')

    class Meta:
        model = OsFamilyComponentModel


class ComponentSchema(ModelSchema):
    kit = fields.Nested('KitSchema', exclude=('components',))
    os = fields.Nested('OperatingSystemSchema')

    class Meta:
        model = ComponentModel


class ResourceAdapterSchema(ModelSchema):
    class Meta:
        model = ResourceAdapterModel


class NodeSchema(ModelSchema):
    softwareprofile = fields.Nested('SoftwareProfileSchema',
                                    only=('id', 'name'))
    hardwareprofile = fields.Nested('HardwareProfileSchema',
                                    only=('id', 'name',
                                          'resourceadapter'))
    nics = fields.Nested('NicSchema', many=True, exclude=('nodes',))

    vcpus = fields.Integer(default=1)

    class Meta:
        model = NodeModel


class SoftwareProfileSchema(ModelSchema):
    nodes = fields.Nested('NodeSchema', many=True,
                          exclude=('softwareprofile',))

    components = fields.Nested('ComponentSchema', many=True,
                               exclude=('softwareprofiles',))

    hardwareprofiles = fields.Nested('HardwareProfileSchema',
                                     only=('id', 'name'), many=True)

    os = fields.Nested('OperatingSystemSchema')

    class Meta:
        model = SoftwareProfileModel


class HardwareProfileSchema(ModelSchema):
    nodes = fields.Nested('NodeSchema', many=True,
                          exclude=('hardwareprofile',))

    mappedsoftwareprofiles = fields.Nested('SoftwareProfileSchema',
                                           only=('id', 'name'), many=True)

    class Meta:
        model = HardwareProfileModel
