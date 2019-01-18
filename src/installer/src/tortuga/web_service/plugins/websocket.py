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

import asyncio
import logging
import os
import ssl
import threading
import tracemalloc
from typing import Optional

import cherrypy
import websockets
from cherrypy.process import plugins

from tortuga.logging import WEBSERVICE_NAMESPACE
from tortuga.web_service.websocket.state_manager import StateManager


logger = logging.getLogger(WEBSERVICE_NAMESPACE)


class WebsocketPlugin(plugins.SimplePlugin):
    """
    A CherryPy plugin that opens a websocket for sending event notifications.

    """
    def __init__(self, scheme: str, port: int, bus, debug: bool = False) -> None:
        super().__init__(bus)
        self._debug = debug

        self.scheme = scheme
        self.port = port

        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None

    def start(self):
        self._thread = threading.Thread(target=self.worker, daemon=True)
        self._thread.start()

    def stop(self):
        self._loop.stop()
        if self._debug:
            tracemalloc.stop()

    def worker(self):
        """
        The thread worker that runs the asyncio event loop for handling
        websockets.

        """
        #
        # Start memory tracing, if debugging is on
        #
        if self._debug:
            tracemalloc.start()

        logger.debug('Starting websocket server thread')

        #
        # Create a new asyncio event loop for the thread
        #
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

        try:
            if self.scheme == 'wss':
                server = self._start_secure()

            elif self.scheme == 'ws':
                server = self._start_insecure()

            else:
                raise Exception(
                    'Unknown websocket scheme: {}'.format(self.scheme))

        except Exception as ex:
            logger.error(str(ex))
            logger.error('Unable to start websocket server')

            return

        #
        # Log memory tracing, if debugging is on
        #
        if self._debug:
            asyncio.ensure_future(memory_stats())

        self._loop.run_until_complete(server)
        self._loop.run_forever()

    def _start_secure(self) -> websockets.WebSocketServerProtocol:
        logger.debug(
            'Starting websocket with SSL/TLS enabled on port {}'.format(
                self.port))

        ssl_context = self._get_ssl_context()

        return websockets.serve(
            websocket_handler, port=self.port, ssl=ssl_context)

    def _get_ssl_context(self) -> ssl.SSLContext:
        cherrypy_cert = cherrypy.config.get('server.ssl_certificate', '')
        cherrypy_key = cherrypy.config.get('server.ssl_private_key', '')
        websocket_cert = cherrypy_cert.replace('.crt', '-bundle.crt')

        if not os.path.exists(websocket_cert):
            raise Exception(
                'Combined SSL cert not found: {}'.format(websocket_cert))

        if not os.path.exists(cherrypy_key):
            raise Exception('SSL key not found: {}'.format(cherrypy_key))

        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(websocket_cert, keyfile=cherrypy_key)
        ssl_context.verify_mode = ssl.CERT_OPTIONAL
        ssl_context.load_default_certs()

        return ssl_context

    def _start_insecure(self) -> websockets.WebSocketServerProtocol:
        logger.debug(
            'Starting websocket with SSL/TLS disabled on port {}'.format(
                self.port))

        return websockets.serve(websocket_handler, port=self.port)


async def memory_stats():
    """
    Prints memory stats to the log, for debugging memory utilization.

    """
    snapshot_initial = tracemalloc.take_snapshot()
    while True:
        await asyncio.sleep(60)
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.compare_to(snapshot_initial, 'lineno')
        for stat in top_stats[:10]:
            logger.debug('Memory: {}'.format(stat))


async def websocket_handler(websocket, path):
    """
    The main websocket handler.

    :param websocket: the websocket server instance
    :param path:      the path requested on the websocket (unused)

    """
    logger.debug('New websocket connection established')

    try:
        state_manager = StateManager(websocket=websocket)
        consumer_task = asyncio.ensure_future(
            state_manager.consumer_handler())
        producer_task = asyncio.ensure_future(
            state_manager.producer_handler())

    except Exception as ex:
        logger.error(str(ex))
        logger.error('Websocket connection exited')
        raise

    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()

    logger.debug('Websocket connection exited')
