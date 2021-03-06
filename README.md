# Epub Unit Converter

The program converts the units in the E-book(Epub) from Imperial to Metric and vice-versa.

![Usage](./usage.png)

## Usage Requirements:
- _Python 3.6_
- [pipenv](https://github.com/pypa/pipenv)

  > Install _pipenv_: `python -m pip install pipenv`

## How to use:
- Clone repo: `git clone https://github.com/kivS/epub_unit_converter.git`

- Enter project folder: `cd epub_unit_converter`

- Install dependencies: `pipenv install`

- Start it up: `pipenv run python init.py`

- Open browser in [`http://localhost:7000`](http://localhost:7000)



## Extras
- You can run the program with arguments to access extra features:

  Argument | Description | Example
  --- | --- | ---
  `-rl` or `--rm-logs` | Resets the logs |`pipenv run python init -rl`
  `-b` or `--open-browser` | Opens app in the default browser | `pipenv run python init.py -b`
  `-d` or `--dev` | Activates Dev mode. \*Requires client's dev web-server to be running | `python run python init.py -d`


## Dev mode
_Dev mode_ activates:
-  debugging info to console and log files in main program
- _client_ with development web-server

### Extra Requirements
- _Nodejs_
- _Npm_ or _Yarn_

### Usage

- Start the main program in dev mode: `pipenv run python init -d`

- In another console window, navigate into client folder: `cd client`

- Install dependencies: `yarn install` or `npm install`

- Run dev web-server: `yarn dev` or `npm run dev`

- Open browser in [`http://localhost:7000`](http://localhost:7000) or open the browser automatically by adding the _browser_ argument when starting the main program.
