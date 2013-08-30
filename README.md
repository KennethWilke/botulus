Botulus
===============
An extensible, pythonic IRC bot

Installation
-----
### Clone your fork
	git clone git@github.com:USER/botulus

### Install requirements

	pip install -r requirements.txt

It is recommended you use a python virtual environment or a virtual server to avoid installing these in your system-wide Python.

Usage
-----
```
usage: botulus.py [-h] [-c CONFIG_PATH] [-H HOST] [-p PORT] [-n NICK]
                  [-s SIGIL] [-r ROOMS] [-m MODULES]
                  [-l {debug,info,warning,error,critical}] [-o OUTPUT] [-d]
                  [-P PIDFILE]

Botulus IRC bot

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config CONFIG_PATH
                        Botulus configuration file(s)
  -H HOST, --host HOST  IRC host address
  -p PORT, --port PORT  IRC host port
  -n NICK, --nick NICK  IRC bot name
  -s SIGIL, --sigil SIGIL
                        Command sigil (Defaults to !)
  -r ROOMS, --rooms ROOMS
                        Comma-separated list of rooms to join at start
  -m MODULES, --modules MODULES
                        Comma-separated list of modules to load at start
  -l {debug,info,warning,error,critical}, --log_level {debug,info,warning,error,critical}
                        Set logging level (warning by default)
  -o OUTPUT, --output OUTPUT
                        Logger output file
  -d, --daemon          Run botulus as a daemon
  -P PIDFILE, --pidfile PIDFILE
                        Path to pidfile for botulus, defaults to
                        /var/run/botulus.pid
```