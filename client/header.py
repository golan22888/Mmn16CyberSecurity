class Header:
    def __init__(self, version, code):
        self.version = version
        self.code = code
        self.payload_size = 0

    def get_version(self):
        return self.version

    def get_code(self):
        return self.code

    def get_payload_size(self):
        return self.payload_size


class RequestHeader(Header):
    def __init__(self, version, code, payload_size):
        super().__init__(version, code)
        self.payload_size = payload_size


class ResponseHeader(Header):
    def __init__(self, client_id, version, code):
        super().__init__(version, code)
        self.client_id = client_id

    def get_client_id(self):
        return self.client_id

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size
