class Event:
    def __init__(self):
        self.connections = []
    def connect(self, callback: callable):
        self.connections.append(callback)
    def emit(self, *args):
        for callback in self.connections:
            callback(*args)