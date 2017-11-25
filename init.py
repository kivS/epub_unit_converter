'''
    

'''

import asyncio
from aiohttp import web
import config


async def ws_handler(request):
    ''' Handles websocket connection'''

    ws = web.WebSocketResponse()

    # Display error if ws fails to start
    if not ws.can_prepare(request):
        print("Well, websocket failed to start..")

    # prepare websocket
    await ws.prepare(request)

    print('Client has connected:', ws)
    ws.send_str('Well hello there Client hero!')

    # go over received message
    async for msg in ws:
        print('Client sent:', msg)

    print('Client has disconnected')
    return ws


async def index_handler(request):
    ''' Returns index page '''
    return web.FileResponse('./index.html')


async def init():
    app = web.Application()

    # routes
    app.router.add_get('/', index_handler)
    app.router.add_get('/wakey_wakey', ws_handler)

    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init())

    # start web server with custom configs
    web.run_app(app, **config.SERVER)
