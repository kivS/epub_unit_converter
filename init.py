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
import warnings
import base64

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

PREVIOUS_CONVERSIONS_REGEXP = re.compile(r'''
    <span \s id="py_epub">   # begining of span tag
    .+                       # converstion text inside span tag
    </span>                  # end of span tag
''', FLAGS)


class ManipulateEpub:
    ''' Class reponsable for transforming the epub file '''

    # string template for text inserted into epub with converted units
    conversion_result_template = '<span id="py_epub">({0})</span>'

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
        self.epub_container: Dict[str, Any] = app['epubs'].setdefault(epub_file_name, {'num_of_content_changes': 0, 'ready': False, 'conversions': []})
        self.ws = app['client']

        self.log_info('Starting...')

    async def start(self):
        ''' Start conversion manipulations on epub file'''
        await self.get_epub_contents()
        await self.remove_previous_conversions()
        await self.convert_epub_contents()
        await self.save_final_epub()

    async def get_epub_contents(self):
        ''' go over each file in the epub & store it in a list with its content '''
        with zipfile.ZipFile(self.epub_obj, 'r') as epub:
            for file in epub.filelist:
                # ignore folders
                if file.is_dir():
                    continue
                # ignore files whose extension is not in the allowed extensions list
                *_, extension = file.filename.split('.')
                if extension not in config.ALLOWED_EPUB_CONTENT_FILE_EXTENSIONS:
                    continue

                self.files_in_epub.append({'name': file.filename, 'content': epub.read(file.filename).decode(), 'content_original_size': file.file_size})

    async def remove_previous_conversions(self):
        ''' go over list of the files in the epub; match & remove previous conversions '''
        for file in self.files_in_epub:
            # replace content of file if it has previous convertions text
            removed_previous_conversions = PREVIOUS_CONVERSIONS_REGEXP.sub('', file['content'])
            if len(removed_previous_conversions) != file['content_original_size']:
                self.log_info('removing previous conversions...')
                file['content'] = removed_previous_conversions

    async def convert_epub_contents(self):
        ''' Go over the epub's files and search all unit regexps for the conversion_unit selected '''
        for file in self.files_in_epub:
            self.log_info(f'Searching file: {file["name"]}')
            for unit in UNIT_CONVERSION_TO[self.conversion_unit]:
                # execute regexp of each unit and store regexp obj in list
                self.log_info(f'Regexp: searching for: {unit["name"]} unit')
                regexp_result = list(unit['regexp'].finditer(file['content']))

                if len(regexp_result) > 0:
                    # let's chill for a moment
                    await asyncio.sleep(0)

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

                            # send convertion result to client
                            converted_text_left_index = converted_unit_text.find('(') + 1  # +1 cuz match includes (
                            converted_text_right_index = converted_unit_text.find(')')
                            conversion_unit_text = 'Imperial <=> Metric' if self.conversion_unit == 'metric' else 'Metric <=> Imperial'
                            result_text_to_client = f'{conversion_unit_text} | {regexp.group()} <=> {converted_unit_text[converted_text_left_index:converted_text_right_index]}'
                            self.epub_container.get('conversions').append(result_text_to_client)
                            self.ws.send_json({
                                'do': 'notify_conversion_update',
                                'with': {
                                    'file': self.epub_file_name,
                                    'conversion': result_text_to_client
                                }
                            })

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

        output_epub_obj: bytes = io.BytesIO()

        with zipfile.ZipFile(self.epub_obj, 'r') as input_epub:
            with zipfile.ZipFile(output_epub_obj, 'w') as output_epub:

                # add files where convertion took place into the final epub
                for file in self.files_in_epub:
                    output_epub.writestr(file['name'], file['content'])

                # add rest of files from epub into the final one
                for file in input_epub.filelist:
                    # ignore files where conversion took place
                    *_, extension = file.filename.split('.')
                    if extension in config.ALLOWED_EPUB_CONTENT_FILE_EXTENSIONS:
                        continue

                    # copy rest of files to final epub file
                    output_epub.writestr(file.filename, input_epub.read(file.filename))

        # save final epub
        self.epub_container['final_epub'] = output_epub_obj.getvalue()
        self.epub_container.update({'ready': True})
        # close epub objects stream
        self.epub_obj.close()
        output_epub_obj.close()

        del self.epub_obj

        # notify user that the epub is done
        self.ws.send_json({
            'do': 'notify_epub_conversion_completed',
            'with': {
                'name': self.epub_file_name,
                'num_of_changes': self.epub_container.get('num_of_content_changes')
            }
        })

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


async def convert_epub(file: dict, app=None):
    ''' .... '''

    # decode epub binary from base64 and remove url metadata(len = 33): data:application/epub+zip;base64,
    # and then load epub binary into memory
    epub_bin = io.BytesIO(base64.b64decode(file['bin_data'][33:]))

    # pass epub bin stream into class responsable for transforming epub
    transform_epub = ManipulateEpub(file['name'], epub_bin, app)

    # clean up
    del file

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

    # if we still have epubs in memory let's make a dict of the epub and send it to the client
    current_epubs: dict = {epub_name: {'ready': epub.get('ready'), 'conversions': epub.get('conversions')} for (epub_name, epub) in request.app.get('epubs').items()}
    if len(current_epubs) > 0:
        ws.send_json({
            'do': 'show_current_epubs',
            'with': current_epubs
        })

    # go over received message
    async for msg in ws:
        log.debug(f'Client sent: {msg}'[:300])

        # convert data to json
        data: Dict[str, Union[str, Dict]] = json.loads(msg.data)

        # handle messages
        if data.get('do') == 'convert_epub':
            file = data.get('with')
            # schedule task for converting epub
            loop.create_task(convert_epub(file, app=request.app))

        elif data.get('do') == 'set_conversion_unit':
            # get conversion unit
            unit_system = data.get('with', 'imperial')

            request.app['conversion_unit'] = unit_system
            log.debug(f'Conversion unit set to {unit_system}')

        elif data.get('do') == 'remove_epub':
            del request.app['epubs'][data.get('with')]

    log.debug('Client has disconnected')
    return ws


async def index_handler(request):
    ''' Returns index page '''
    return web.FileResponse('./index.html')


async def epub_download_handler(request):
    epub_name: str = request.match_info.get('epub_name')

    epub: dict = request.app.get('epubs').get(epub_name)

    if not epub_name or not epub:
        return web.Response(text='nope')

    return web.Response(body=epub.get('final_epub'), content_type='application/epub+zip')


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
    app.router.add_get('/download_epub/{epub_name}', epub_download_handler)

    # signals
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":

    loop = asyncio.get_event_loop()

    # get parsed commandline arguments
    args = config.ARGS_PARSER.parse_args()

    if args.debug:

        # set loop debug
        loop.set_debug(True)

        # Report all mistakes managing asynchronous resources.
        warnings.simplefilter('always', ResourceWarning)

        # set all loggers to debug level
        for logger_name in config.LOGGING['loggers'].keys():
            logging.getLogger(logger_name).setLevel(logging.DEBUG)

    app = loop.run_until_complete(init())

    UREG: pint.UnitRegistry = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)

    print(f'''
        ======== Running on http://localhost:{config.SERVER.get("port", 7000)} ========
                        (Press CTRL+C to quit)
    ''')

    # start web server with custom configs
    web.run_app(app, **config.SERVER)
