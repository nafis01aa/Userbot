prefixes = ['/', '.', ',', '!']

class BotCommands:
    def __init__(self):
        self.start = (['start'], prefixes)
        self.help = (['help'], prefixes)
        self.ping = (['ping'], prefixes)
        self.yo = (['yo'], prefixes)

        self.alive = (['alive'], prefixes)
        self.id = (['id'], prefixes)
        self.pmstop = (['stop'], prefixes)
        self.restrictforwarder = (['forward', 'copymsg'], prefixes)

UCommand = BotCommands()
