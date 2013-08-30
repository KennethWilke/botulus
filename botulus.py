#!/usr/bin/python2.7
from botulus import Botulus
import ast
import argparse
from ConfigParser import SafeConfigParser, NoSectionError
import sys
import logging
import os
from daemonize import Daemonize

# Argument parsing options
argparser = argparse.ArgumentParser(description="Botulus IRC bot")
argparser.add_argument('-c', '--config', metavar="CONFIG_PATH",
                       action='append', help="Botulus configuration file(s)")
argparser.add_argument('-H', '--host', help="IRC host address")
argparser.add_argument('-p', '--port', type=int, help="IRC host port")
argparser.add_argument('-n', '--nick', help="IRC bot name")
argparser.add_argument('-s', '--sigil', help="Command sigil (Defaults to !)")
argparser.add_argument('-r', '--rooms',
                       help="Comma-separated list of rooms to join at start")
argparser.add_argument('-m', '--modules',
                       help="Comma-separated list of modules to load at start")
argparser.add_argument('-l', '--log_level', choices=['debug', 'info',
                                                     'warning', 'error',
                                                     'critical'],
                       help="Set logging level (warning by default)")
argparser.add_argument('-o', '--output', help="Logger output file")
argparser.add_argument('-d', '--daemon', help="Run botulus as a daemon",
                       action='store_true')
argparser.add_argument('-P', '--pidfile',
                       help="Path to pidfile for botulus, defaults to " +
                            "/var/run/botulus.pid")
args = argparser.parse_args()

# Load configuration files
parser = SafeConfigParser()
if args.config:
    for config_file in args.config:
        parser.read(config_file)

# Set logger level based on cli or config
if args.log_level:
    log_level = getattr(logging, args.log_level.upper())
elif parser.has_option('irc', 'log_level'):
    if parser.get('irc', 'log_level') in ['debug', 'info', 'warning', 'error',
                                          'critical']:
        log_level = getattr(logging, parser.get('irc', 'log_level').upper())
else:
    log_level = logging.WARNING

if args.output:
    logfile = args.output
else:
    logfile = None

# Set sigil to cli if given, else use sigil in config files, else use default !
if args.sigil:
    sigil = args.sigil
elif parser.has_option('irc', 'sigil'):
    sigil = parser.get('irc', 'sigil')
else:
    sigil = '!'

# Grab channels from config
channels = {}
if parser.has_section('channels'):
    for k, v in parser.items('channels'):
        channels[k] = ast.literal_eval(v)
# Grab channels from args
if args.rooms:
    for channel in args.rooms.split(','):
        channels[channel] = {}

# Set host based on argument first, config second
if args.host:
    host = args.host
elif parser.has_option('irc', 'host'):
    host = parser.get('irc', 'host')
else:
    print "No hostname provided via arguments or configuration"
    sys.exit(1)

# Set port by argument first, config second, or default to 6667
if args.port:
    port = args.port
elif parser.has_option('irc', 'port'):
    port = parser.get('irc', 'port')
else:
    port = 6667

# Set bot nickname by argument first, config second, or default to Botulus
if args.nick:
    nick = args.nick
elif parser.has_option('irc', 'nick'):
    nick = parser.get('irc', 'nick')
else:
    nick = "Botulus"

# Load botulus object
bot = Botulus(host, port, nick, channels, sigil, logfile, log_level)

# Load modules
if parser.has_section('modules'):
    for target, module in parser.items('modules'):
        bot.load_module(target, module)
if args.modules:
    for module in args.modules.split(','):
        bot.load_module(module, module)

# Start the bot
if args.daemon:
    if args.pidfile:
        pidfile = args.pidfile
    else:
        pidfile = "/var/run/botulus.pid"
    if os.path.exists(pidfile):
        print "Pidfile '%s' already exists" % pidfile
        sys.exit(1)
    # Test if writable
    try:
        with open(pidfile, 'w'):
            pass
    except Exception as error:
        print "Failed to create pidfile\n%s" % error
        sys.exit(1)
    # Delete write test
    os.unlink(pidfile)
    # Start deamon
    daemon = Daemonize(app="botulus", action=bot.run, pid=pidfile)
    daemon.start()
else:
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.module_cleanup()
        print "Botulus shutdown"
