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
import re


FLAGS = re.VERBOSE | re.IGNORECASE | re.MULTILINE


def build_regexp(unit_regexp):
    return re.compile(r'''
            (?P<value>       # group name: value
                \d+
            )
            [ ]*             # match zero or more spaces between the value and the unit
            (?P<unit>        # group name: unit
                {0}          # specific unit regular expression
            )
            \b               # make sure it ends in a word
        '''.format(unit_regexp), FLAGS)


UNIT_CONVERSION_TO = {
    'metric': [
        {
            'name': 'Pounds',
            'convertsTo': 'kg',
            'regexp': build_regexp(r'''
                    lbs
                    | lb
                    | lbm
                    | pound[s]?  # get plural or singular form
                ''')
        },
        {
            'name': 'Inches',
            'convertsTo': 'cm',
            'regexp': build_regexp(r'''
                    inch(?:es)? # match group for plural-dont capture- or singular form
                ''')
        },
        {
            'name': 'Foot',
            'convertsTo': 'm',
            'regexp': build_regexp(r'''
                    foot
                    | feet
                    | ft
                ''')
        },
        {
            'name': 'Yard',
            'convertsTo': 'm',
            'regexp': build_regexp(r'''
                    yard[s]?  # get plural or singular form
                    | yd
                ''')
        },
        {
            'name': 'Gallon',
            'convertsTo': 'liters',
            'regexp': build_regexp(r'''
                   gal
                   | gallon[s]?  # get plural or singular form
                ''')
        },
        {
            'name': 'Ounce',
            'convertsTo': 'g',
            'regexp': build_regexp(r'''
                    oz
                    | ounce[s]?
                ''')
        },
        {
            'name': 'Fahrenheit',
            'convertsTo': 'celcius',
            'regexp': build_regexp(r'''
                    fahrenheit
                    | f
                ''')
        },

    ],
    'imperial': [
        {
            'name': 'Meter',
            'convertsTo': 'feet',
            'regexp': build_regexp(r'''
                                m
                                | meter[s]?  #  match unit - meter or meters
                        ''')
        },
        {
            'name': 'Kilogram',
            'convertsTo': 'lbs',
            'regexp': build_regexp(r'''
                               kg
                               | kilogram[s]? # match plural or singular
                               | kilogramme
                        ''')
        },
        {
            'name': 'Kilometer',
            'convertsTo': 'miles',
            'regexp': build_regexp(r'''
                                km
                                | kilometer[s]?
                        ''')
        },
        {
            'name': 'Centimeter',
            'convertsTo': 'inch',
            'regexp': build_regexp(r'''
                                cm
                                | centimeter[s]?
                        ''')
        },
        {
            'name': 'Liter',
            'convertsTo': 'gal',
            'regexp': build_regexp(r'''
                                liter[s]?
                                | l
                        ''')
        },
        {
            'name': 'Gram',
            'convertsTo': 'oz',
            'regexp': build_regexp(r'''
                                gram[s]?
                                | g
                        ''')
        },
        {
            'name': 'Celcius',
            'convertsTo': 'fahrenheit',
            'regexp': build_regexp(r'''
                                c
                                | celcius
                                | °C
                        ''')
        }
    ]
}


class ManipulateEpub:
    ''' Class reponsable for transforming the epub file '''

    def __init__(self, epub_file_name, epub_obj, app):
        self.epub_file_name = epub_file_name
        self.epub_obj = epub_obj
        self.files_in_epub = []
        self.conversion_unit = app.get('conversion_unit')
        self.logger = logging.getLogger('app')
        self.tag = f'Epub:[{epub_file_name}] | -'

        self.log_info('Starting...')

    async def start(self):
        await self.get_epub_contents()
        await self.convert_epub_contents()

    def log_info(self, msg):
        self.logger.info(f'{self.tag} {msg}')

    async def get_epub_contents(self):
        ''' go over each file in the epub & store it in a list with its content '''
        with zipfile.ZipFile(self.epub_obj, 'r') as epub:
            for file in epub.filelist:
                # ignore folders
                if file.is_dir():
                    continue
                self.files_in_epub.append({'name': file.filename, 'content': epub.read(file.filename).decode(), 'content_original_size': file.file_size})

    async def convert_epub_contents(self):
        ''' Go over the epub's files and search all unit regexps for the conversion_unit selected '''
        for file in self.files_in_epub:
            self.log_info(f'Searching file: {file["name"]}')
            for unit in UNIT_CONVERSION_TO[self.conversion_unit]:
                # execute regexp of each unit and store regexp obj in list
                self.log_info(f'Regexp: searching for: {unit["name"]} unit')
                regexp_result = list(unit['regexp'].finditer(file['content']))

                if len(regexp_result) > 0:
                    self.log_info(f'Regexp result: {regexp_result}')

                    for regexp in regexp_result:
                        converted_unit = '<span>(<--- PlaceHolder For Converted Text --->)</span>'

                        # replace content for: text till position of matched text + converted text + text after the position of the matched text
                        file['content'] = file['content'][:regexp.end()] + converted_unit + file['content'][regexp.end():]

                else:
                    self.log_info('Regexp: No result found...')


async def convert_epub(file_name, loop=None, app=None):
    ''' .... '''
    ws = app.get('client')
    log = logging.getLogger('app')

    if not os.path.exists(file_name):
        ws.send_str(f'File not found: {file_name}')
    else:
        # open file
        log.debug(f'opening file: [{file_name}]')
        async with aiofiles.open(file_name, 'rb') as f:
            file_bin = await f.read()

        # get epub name of out the path & remove extension
        epub_name = os.path.basename(file_name)
        epub_name, _ = os.path.splitext(epub_name)

        # pass epub bin stream into class responsable for transforming epub
        transform_epub = ManipulateEpub(epub_name, io.BytesIO(file_bin), app)

        # clean up
        del f, file_bin

        # start epub transformations
        await transform_epub.start()


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

        elif data.get('do') == 'set_conversion_unit':
            # get conversion unit
            unit_system = data.get('with', 'imperial')

            request.app['conversion_unit'] = unit_system
            log.debug(f'Conversion unit set to {unit_system}')

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
