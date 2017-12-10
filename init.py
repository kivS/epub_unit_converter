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
import pint
from typing import List, Dict, Union, Any


FLAGS = re.VERBOSE | re.IGNORECASE | re.MULTILINE


def build_regexp(unit_regexp: str):
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
            'name': 'pounds',
            'convertsTo': 'kg',
            'regexp': build_regexp(r'''
                    lbs
                    | lb
                    | pound[s]?  # get plural or singular form
                ''')
        },
        {
            'name': 'inches',
            'convertsTo': 'cm',
            'regexp': build_regexp(r'''
                    inch(?:es)? # match group for plural-dont capture- or singular form
                ''')
        },
        {
            'name': 'foot',
            'convertsTo': 'm',
            'regexp': build_regexp(r'''
                    foot
                    | feet
                    | ft
                ''')
        },
        {
            'name': 'yard',
            'convertsTo': 'm',
            'regexp': build_regexp(r'''
                    yard[s]?  # get plural or singular form
                    | yd
                ''')
        },
        {
            'name': 'gallon',
            'convertsTo': 'liters',
            'regexp': build_regexp(r'''
                   gal
                   | gallon[s]?  # get plural or singular form
                ''')
        },
        {
            'name': 'ounce',
            'convertsTo': 'g',
            'regexp': build_regexp(r'''
                    oz
                    | ounce[s]?
                ''')
        },
        {
            'name': 'fahrenheit',
            'convertsTo': 'celsius',
            'regexp': build_regexp(r'''
                    fahrenheit
                    | °F
                ''')
        },

    ],
    'imperial': [
        {
            'name': 'meter',
            'convertsTo': 'feet',
            'regexp': build_regexp(r'''
                                m
                                | meter[s]?  #  match unit - meter or meters
                        ''')
        },
        {
            'name': 'kilogram',
            'convertsTo': 'lbs',
            'regexp': build_regexp(r'''
                               kg
                               | kilogram[s]? # match plural or singular
                        ''')
        },
        {
            'name': 'kilometer',
            'convertsTo': 'miles',
            'regexp': build_regexp(r'''
                                km
                                | kilometer[s]?
                        ''')
        },
        {
            'name': 'centimeter',
            'convertsTo': 'inch',
            'regexp': build_regexp(r'''
                                cm
                                | centimeter[s]?
                        ''')
        },
        {
            'name': 'liter',
            'convertsTo': 'gal',
            'regexp': build_regexp(r'''
                                liter[s]?
                                | l
                        ''')
        },
        {
            'name': 'gram',
            'convertsTo': 'oz',
            'regexp': build_regexp(r'''
                                gram[s]?
                                | g
                        ''')
        },
        {
            'name': 'celsius',
            'convertsTo': 'fahrenheit',
            'regexp': build_regexp(r'''
                                celsius
                                | °C
                        ''')
        }
    ]
}


class ManipulateEpub:
    ''' Class reponsable for transforming the epub file '''

    # string template for text inserted into epub with converted units
    conversion_result_template = '<span id="py_epub">{0}</span>'

    def __init__(self, epub_file_name: str, epub_obj: io.BytesIO, app) -> None:
        self.epub_file_name = epub_file_name
        self.epub_obj = epub_obj
        # files in epub that will be processed
        self.files_in_epub: List[Dict[str, Union[str, int]]] = []
        self.conversion_unit: str = app.get('conversion_unit')
        self.logger = logging.getLogger('app')
        self.tag: str = f'Epub:[{epub_file_name}] | -'
        # add epub container containing meta data and eventually the final epub file
        # set number of the counter of the changes made to the epub's contents to 0
        self.epub_container: Dict[str, Union[int, bytes]] = app['epubs'].setdefault(epub_file_name, {'num_of_content_changes': 0})

        self.log_info('Starting...')

    async def start(self):
        ''' Start conversion manipulations on epub file'''
        await self.get_epub_contents()
        await self.convert_epub_contents()
        await self.save_final_epub()

    async def get_epub_contents(self):
        ''' go over each file in the epub & store it in a list with its content '''
        with zipfile.ZipFile(self.epub_obj, 'r') as epub:
            for file in epub.filelist:
                # ignore folders
                if file.is_dir():
                    continue
                # ignore files whose extension in not in the allowed extensions list
                *_, extension = file.filename.split('.')
                if extension not in config.ALLOWED_EPUB_CONTENT_FILE_EXTENSIONS:
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

                    # go over each regexp result on current file
                    for regexp in regexp_result:

                        try:
                            # parse regexp result value into Pint
                            pint_parsed_value = UREG(f'{regexp.group("value")} {unit["name"]}')
                            # Convert to metric/imperial counterpart
                            converted_unit = pint_parsed_value.to(unit["convertsTo"])
                        except Exception as e:
                            self.log_error(e)
                            continue
                        else:
                            # fill the string template with the converted & formated value with unit string
                            converted_unit_text = self.conversion_result_template.format(self.format_unit(converted_unit, unit["convertsTo"]))
                            self.log_info(f'Regexp Result: {regexp.group()} | Converts to: {converted_unit_text}')

                            # replace content with new string containing the converted unit
                            file['content'] = file['content'][:regexp.end()] + converted_unit_text + file['content'][regexp.end():]
                            # add +1 to changes made to epub file
                            self.epub_container['num_of_content_changes'] += 1
                else:
                    self.log_info('Regexp: No result found...')

        self.log_info('Done.')
        self.log_info(f'Number of changes: {self.epub_container["num_of_content_changes"]}')

    async def save_final_epub(self):
        ''' Update epub file with changes made by conversion & save final epub to globals '''
        with zipfile.ZipFile(self.epub_obj, 'w') as epub:
            for file in self.files_in_epub:
                # ignore files whose content has not changed
                if len(file['content']) == file['content_original_size']:
                    continue

                # replace file in epub(zipfile)
                epub.writestr(file['name'], file['content'])

        # save final epub
        self.epub_container['final_epub'] = self.epub_obj.getvalue()
        # close epub_obj stream
        self.epub_obj.close()
        self.log_info('All done, final epub saved!')

    def format_unit(self, converted_unit: Any, convertsTo: str) -> str:
        '''
            given a converted_unit object & the unit it converts to,
            return a string where the value is rounded.
        '''
        precision_of_digits = 2
        rounded_magnitude = round(converted_unit.magnitude, precision_of_digits)
        # add dynamic sapce depending on the length of the result unit
        text_separator = '' if len(convertsTo) < 2 else ' '

        return f'{rounded_magnitude}{text_separator}{convertsTo}'

    def log_info(self, msg):
        self.logger.info(f'{self.tag} {msg}')

    def log_error(self, msg):
        self.logger.error(f'{self.tag} {msg}')


async def convert_epub(file_location: str, app=None):
    ''' .... '''
    ws = app.get('client')
    log = logging.getLogger('app')

    if not os.path.exists(file_location):
        ws.send_str(f'File not found: {file_location}')
    else:
        # open file
        log.debug(f'opening file: [{file_location}]')
        async with aiofiles.open(file_location, 'rb') as f:
            file_bin = await f.read()

        # get epub name of out the path & remove extension
        epub_name = os.path.basename(file_location)
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
        data: Dict[str, Union[str, Dict]] = json.loads(msg.data)

        # handle messages
        if data.get('do') == 'convert_epub':
            file_location = data.get('with')

            # schedule task for converting epub
            loop.create_task(convert_epub(file_location, app=request.app))

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

    UREG: pint.UnitRegistry = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init())

    print(f'''
        ======== Running on http://localhost:{config.SERVER.get("port", 7000)} ========
                        (Press CTRL+C to quit)
    ''')

    # start web server with custom configs
    web.run_app(app, **config.SERVER)
