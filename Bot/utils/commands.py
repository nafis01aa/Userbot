prefixes = ['/', '.', ',', '!']

class BotCommands:
    def __init__(self):
        self.help = (['help'], prefixes)
        self.start = (['start'], prefixes)

class UserCommands:
    def __init__(self):
        self.alive = (['alive'], prefixes)
        self.ban = (['ban'], prefixes)
        self.gban = (['gban'], prefixes)
        self.help = (['help'], prefixes)
        self.id = (['id'], prefixes)
        self.log = (['log', 'logs'], prefixes)
        self.mute = (['mute'], prefixes)
        self.ping = (['ping'], prefixes)
        self.pmstop = (['stop'], prefixes)
        self.purge = (['purge'], prefixes)
        self.restrictforwarder = (['forward', 'copymsg'], prefixes)
        self.unban = (['unban'], prefixes)
        self.unmute = (['unmute'], prefixes)
        self.yo = (['yo'], prefixes)

BCommand = BotCommands()
UCommand = UserCommands()
