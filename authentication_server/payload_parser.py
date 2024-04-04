from abc import ABC, abstractmethod
import struct
import payload as p


class PayloadParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data):
        pass


class RegisterPayloadParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< {p.CLIENT_NAME_SIZE}s {p.CLIENT_PASSWORD_SIZE}s'

    @staticmethod
    def parse(data):
        try:
            name, password = struct.unpack(RegisterPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
            payload = p.RequestUserPayload(name.rstrip(b'\x00').decode('utf-8'),
                                           password.rstrip(b'\x00').decode('utf-8'))
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing payload in authentication server')


class RequestSymKeyPayloadParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< {p.SERVER_ID_SIZE}s {p.NONCE_SIZE}s'

    @staticmethod
    def parse(data):
        try:
            server_id, nonce = struct.unpack(RequestSymKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
            payload = p.RequestSymKeyPayload(server_id, nonce)
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing payload')
