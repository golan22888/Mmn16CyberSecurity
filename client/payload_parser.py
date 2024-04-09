from abc import ABC, abstractmethod
import struct
import payload as p
from encrypted_key import DecryptedEncryptedKey
import uuid


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
            payload = p.ReceiveRegistrationSucceededPayload(uuid.UUID(bytes=client_id))
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the client id in client')


class SymKeyAndTicketParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = (
        f'< {p.CLIENT_ID_SIZE}s {p.ENCRYPTED_KEY_IV_SIZE}s {p.AES_CBC_BLOCK_SIZE}s {3 * p.AES_CBC_BLOCK_SIZE}s'
        f' {121}s ')

    @staticmethod
    def parse(data):
        try:
            (client_id, encrypted_key_iv, nonce, encrypted_key_aes_key, ticket) = (
                struct.unpack(
                    SymKeyAndTicketParser.PROTOCOL_PAYLOAD_FORMAT, data))
            password = input("Enter your password: ")
            decrypted_key = DecryptedEncryptedKey(encrypted_key_iv, nonce, encrypted_key_aes_key, password)
            serialized_ticket = ticket
            payload = p.ReceiveSymKeyAndTicketPayload(uuid.UUID(bytes=client_id), decrypted_key,
                                                      serialized_ticket)
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the symmetric key and ticket in client')


class EmptyPayload(PayloadParser):
    @staticmethod
    def parse(data):
        return p.EmptyPayload
