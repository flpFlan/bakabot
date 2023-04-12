class EventArgs:
    canceled: bool = False


class Event:
    def __init__(self):
        self._ = EventArgs()

    def cancel(self):
        self._.canceled = True
