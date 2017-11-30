'''
    

'''

import asyncio
from aiohttp import web
import aiofiles
import config
import json
import os
import logging
import io
import zipfile


async def convert_epub(file_name, loop=None, app=None):
    ''' .... '''
    ws = app.get('client')
    log = logging.getLogger('app')

    # check if file exists.
    if not os.path.exists(file_name):
        ws.send_str(f'File not found: {file_name}')
    else:
        # open file
        log.debug(f'opening file: [{file_name}]')
        async with aiofiles.open(file_name, 'rb') as f:
            file_bin = await f.read()

        # get basename of epub file
        epub_name = os.path.basename(file_name)
        # remove extension
        epub_name, _ = os.path.splitext(epub_name)

        # save zipfile in memory
        app['epubs'][epub_name] = zipfile.ZipFile(io.BytesIO(file_bin))


async def ws_handler(request):
    ''' Handles websocket connection'''

    log = request.app.logger
    loop = request.app.loop

    ws = web.WebSocketResponse()

    # Display error if ws fails to start
    if not ws.can_prepare(request):
        log.error("Well, websocket failed to start..")

    # prepare websocket
    await ws.prepare(request)

    # save ws client
    request.app['client'] = ws

    log.debug('Client has connected')
    ws.send_str('Well hello there Client hero!')

    # go over received message
    async for msg in ws:
        log.debug(f'Client sent: {msg}')

        # convert data to json
        data = json.loads(msg.data)

        # handle messages
        if data.get('do') == 'convert_epub':
            file_name = data.get('with')

            # schedule task for converting epub
            loop.create_task(convert_epub(file_name, app=request.app, loop=loop))

        elif data.get('do') == 'set_convertion_unit':
            # get convertion unit
            unit_system = data.get('with', 'imperial')

            request.app['convertion_unit'] = unit_system
            log.debug(f'Convertion unit set to {unit_system}')

    log.debug('Client has disconnected')
    return ws


async def index_handler(request):
    ''' Returns index page '''
    return web.FileResponse('./index.html')


async def on_shutdown(app):
    ''' On app shutdown '''

    # close client websocket
    client_ws = app.get('client')
    if client_ws:
        await client_ws.close()


async def init():
    ''' Server init config '''
    app = web.Application()

    # init globals
    app['epubs'] = {}

    # routes
    app.router.add_get('/', index_handler)
    app.router.add_get('/wakey_wakey', ws_handler)

    # signals
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init())

    # start web server with custom configs
    web.run_app(app, **config.SERVER)
