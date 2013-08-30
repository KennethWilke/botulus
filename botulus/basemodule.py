class BaseModule(object):
    def __init__(self, bot):
        self.parent = bot

    def __call__(self, event, args):
        if len(args) == 1:
            if hasattr(self, 'default'):
                self.parent.reply(event, self.default())
            elif hasattr(self, 'help'):
                self.parent.reply(event, self.help())
        else:
            if not args[1].startswith('_') and hasattr(self, args[1]):
                function = getattr(self, args[1])
                if len(args) > 2:
                    self.parent.reply(event, function(args[2:]))
                else:
                    self.parent.reply(event, function())
            else:
                if hasattr(self, 'default'):
                    self.parent.reply(event, self.default(args[1:]))
                else:
                    self.parent.reply(event, '%s has no %s command' % (args[0], args[1]))
