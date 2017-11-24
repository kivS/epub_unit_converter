'''
    

'''

import asyncio
from aiohttp import web
import config


async def ws_handler(request):
    ''' Handles websocket connection'''
    return web.Response(text="HUHH, What's up doc?")


async def index_handler(request):
    ''' Returns index page '''
    return web.FileResponse('./index.html')


async def init(loop):
    app = web.Application()

    # routes
    app.router.add_get('/', index_handler)
    app.router.add_get('/wakey_wakey', ws_handler)

    return app


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))

    # start web server with custom configs
    web.run_app(app, **config.SERVER)
