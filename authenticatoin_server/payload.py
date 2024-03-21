from abc import ABC

CLIENT_NAME_SIZE = 255

class Payload(ABC):
    pass

class RequestUserPayload(Payload):
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

