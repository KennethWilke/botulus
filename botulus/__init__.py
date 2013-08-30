# External dependencies
import irc.bot
import importlib
import time
import logging
import datetime
import os
from multiprocessing import Process

logger = logging.getLogger('botulus')


class Botulus(irc.bot.SingleServerIRCBot):
    """ Main bot class """

    def __init__(self, host, port=6667, nick="Botulus", channels=None,
                 sigil="!", logfile=None,
                 log_level=logging.WARNING):
        """ Initialize the bot """
        self.host = host
        self.port = int(port)
        self.nick = nick
        self.channel_settings = channels
        self.handlers = {}
        self.sigil = sigil
        self.logfile = logfile
        self.log_level = log_level

    def run(self):
        irc.bot.SingleServerIRCBot.__init__(self,
                                            [(self.host, self.port)],
                                            self.nick,
                                            self.nick)
        if self.logfile:
            fh = logging.FileHandler(self.logfile)
            fh.setLevel(self.log_level)
            logger.addHandler(fh)
        self.start()

    def load_module(self, target, module):
        """ Load a module for use in Botulous"""
        logger.info('Loading %s' % module)
        try:
            mod = importlib.import_module("modules.%s" % module)
        except Exception as e:
            print "Error loading module: %s" % e
            logger.error("Error loading module: %s" % e)

        self.handlers[target] = mod.__module__(self)

    def on_welcome(self, connection, event):
        """ This function is an event handler that joins rooms upon receiving
        the irc welcome message """
        self.connection = connection
        for i in self.channel_settings:
            self.join(i)

    def join(self, room):
        """ This function will make the irc bot join the given room """
        if not room.startswith('#'):
            room = '#' + room
        logger.info("Joining room %s" % room)
        self.connection.join(room)

    def on_nicknameinuse(self, c, e):
        """ This function prepends an underscore if the bot name is already in
        use """
        oldnick = c.get_nickname()
        logger.warning("Nickname '%s' was already in use," % oldnick +
               " appending underscore")
        c.nick(oldnick + "_")

    def reply(self, e, msg):
        """ This message replies to the source of the event """
        if e.target.startswith('#'):
            for i in msg.split('\n'):
                message = "%s: %s" % (e.source[:e.source.find('!')], i)
                self.connection.privmsg(e.target, message)
                time.sleep(.2)
        else:
            for i in msg.split('\n'):
                self.connection.privmsg(e.source[:e.source.find('!')], i)
                time.sleep(.2)

    def process_command(self, c, e, cmd):
        """ This function looks for the command to process and executes it """
        if cmd[0] in self.handlers:
            try:
                proc = Process(target=self.handlers[cmd[0]], args=(e, cmd))
                proc.start()
            except Exception as ex:
                self.reply(e, "Error running command: %r" % ex)
        else:
            self.reply(e, "Unknown command/module")

    def on_pubmsg(self, c, e):
        """ This is the public message event handler """
        if 'logging' in self.channel_settings[e.target[1:]]:
            channel = e.target[1:]
            if self.channel_settings[channel]['logging']:
                today = datetime.datetime.today()
                time_format = "(%m/%d/%y %I:%M%p)"
                with open('logs/%s.log' % channel, 'a') as channel_log:
                    user = e.source[:e.source.find('!')]
                    message = e.arguments[0]
                    channel_log.write('%s <%s>: %s\n' %
                                      (today.strftime(time_format),
                                      user, message))
        attempt_command = (e.arguments[0].startswith(self.sigil)
                           and len(e.arguments[0]) > (len(self.sigil) + 1))
        if attempt_command:
            cmd = e.arguments[0][len(self.sigil):].split()
            self.process_command(c, e, cmd)

    def on_privmsg(self, c, e):
        """ This is the private message event handler """
        self.process_command(c, e, e.arguments[0].split())

    def module_cleanup(self):
        """ This function cleans up after loaded modules """
        for module in self.handlers:
            if hasattr(module, '__cleanup__'):
                module.__cleanup__()
