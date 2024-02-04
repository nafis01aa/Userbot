prefixes = ['/', '.', ',', '!']

class UserCommands:
    def __init__(self):
        self.help = (['help'], prefixes)
        self.ping = (['ping'], prefixes)
        self.yo = (['yo'], prefixes)

        self.alive = (['alive'], prefixes)
        self.ban = ()
        self.gban = ()
        self.id = (['id'], prefixes)
        self.mute = ()
        self.pmstop = (['stop'], prefixes)
        self.purge = ()
        self.restrictforwarder = (['forward', 'copymsg'], prefixes)
        self.unban = ()
        self.unmute = ()

UCommand = UserCommands()
