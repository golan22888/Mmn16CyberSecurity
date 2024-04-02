from abc import ABC, abstractmethod
import struct
import payload as p



class PayloadParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data):
        pass


class RegistrationSucceededParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< {p.CLIENT_ID_SIZE}s'

    @staticmethod
    def parse(data):
        try:
            client_id = struct.unpack(RegistrationSucceededParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
            payload = p.ResponseToRegistrationSucceededPayload(client_id.rstrip(b'\x00').decode('utf-8'))
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the client id in client')


class SymKeyAndTicketParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = (f'< {p.CLIENT_ID_SIZE}s {p.ENCRYPTED_KEY_IV_SIZE}s {p.NONCE_SIZE}s {p.AES_KEY_SIZE}s'
                               f'{p.VERSION_SIZE}s {p.CLIENT_ID_SIZE}s {p.SERVER_ID_SIZE}s {p.CREATION_TIME_SIZE}s'
                               f'{p.TICKET_IV_SIZE}s {p.AES_KEY_SIZE}s {p.EXPIRATION_TIME_SIZE}s')

    @staticmethod
    def parse(data):
        try:
            (client_id, encrypted_key_iv, nonce, encrypted_key_aes_key, version, ticket_client_id, server_id,
             creation_time, ticket_iv, ticket_aes_key, expiration_time) = struct.unpack(
                RegistrationSucceededParser.PROTOCOL_PAYLOAD_FORMAT, data)

            payload = p.ResponseToRegistrationSucceededPayload(client_id.rstrip(b'\x00').decode('utf-8'))
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the client id in client')
