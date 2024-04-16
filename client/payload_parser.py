from abc import ABC, abstractmethod
import struct
import payload as p
from encrypted_key import DecryptedEncryptedKey
import uuid
import client_constant as c


class PayloadParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data, nonce):
        pass


class RegistrationSucceededParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< {c.CLIENT_ID_SIZE}s'

    @staticmethod
    def parse(data, nonce):
        try:
            client_id = struct.unpack(RegistrationSucceededParser.PROTOCOL_PAYLOAD_FORMAT, data)[0]
            payload = p.ReceiveRegistrationSucceededPayload(uuid.UUID(bytes=client_id))
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the client id in client')


class SymKeyAndTicketParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = (
        f'< {c.CLIENT_ID_SIZE}s {c.ENCRYPTED_KEY_IV_SIZE}s {c.AES_CBC_BLOCK_SIZE}s {3 * c.AES_CBC_BLOCK_SIZE}s'
        f' {c.DECRYPTED_TICKET_SIZE}s ')

    @staticmethod
    def parse(data, my_nonce):
        nonce_to_check = None
        i = 0
        try:
            (client_id, encrypted_key_iv, nonce, encrypted_key_aes_key, ticket) = (
                struct.unpack(
                    SymKeyAndTicketParser.PROTOCOL_PAYLOAD_FORMAT, data))
            while i < 3 and my_nonce != nonce_to_check:
                text = "Enter your password: " if i == 0 else "incorrect password. Try again: "
                password = input(text)
                decrypted_key = DecryptedEncryptedKey(encrypted_key_iv, nonce, encrypted_key_aes_key, password)
                nonce_to_check = decrypted_key.get_nonce()
                i += 1
            if i == 3 and my_nonce != nonce_to_check:
                print("Invalid password")
            else:
                serialized_ticket = ticket
                payload = p.ReceiveSymKeyAndTicketPayload(uuid.UUID(bytes=client_id), decrypted_key,
                                                      serialized_ticket)
                return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing the symmetric key and ticket in client')


class EmptyPayload(PayloadParser):
    @staticmethod
    def parse(data, nonce):
        return p.EmptyPayload
