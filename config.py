'''
    Configs
'''

# SERVER params
# https://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.run_app
SERVER = {
    'port': 7000
}
SERVER['print'] = print(f'''
    ======== Running on http://localhost:{SERVER.get("port", 7000)} ========
                    (Press CTRL+C to quit)
''')
