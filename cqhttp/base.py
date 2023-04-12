class EventArgs:
    canceled: bool = False


class Event:
    _ = EventArgs()

    def cancel(self):
        self._.canceled = True
