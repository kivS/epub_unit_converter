'''
    

'''

import asyncio
from aiohttp import web
import config


async def ws_handler(request):
    ''' Handles websocket connection'''

    log = request.app.logger

    ws = web.WebSocketResponse()

    # Display error if ws fails to start
    if not ws.can_prepare(request):
        log.error("Well, websocket failed to start..")

    # prepare websocket
    await ws.prepare(request)

    # save ws client
    request.app['client'] = ws

    log.info('Client has connected')
    ws.send_str('Well hello there Client hero!')

    # go over received message
    async for msg in ws:
        log.info(f'Client sent: {msg}')

    log.info('Client has disconnected')
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
