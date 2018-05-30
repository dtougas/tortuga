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

import datetime

import cherrypy

from tortuga.web_service.auth.decorators import authentication_required

from .tortugaController import TortugaController


class RootController(TortugaController):
    """
    Root controller class

    """
    actions = [
        {
            'name': 'getNodeList',
            'path': '/ping',
            'action': 'ping',
            'method': ['GET']
        },
    ]

    @cherrypy.tools.json_out()
    @authentication_required()
    def ping(self, **kwargs):
        """
        """
        return {'message': 'hello'}