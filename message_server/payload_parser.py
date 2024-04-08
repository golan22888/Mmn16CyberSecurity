import math
from abc import ABC, abstractmethod
import struct
import payload as p
from decrypted_authenticator import DecryptedAuthenticator
from decrypted_ticket import DecryptedTicket


class PayloadParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data):
        pass


class SymKeyPayloadParser(PayloadParser):
    # version, client_id, server_id, creation_time, aes_key, expiration_time -> are encrypted, so we need to take their
    # sizes with the padded data
    PROTOCOL_PAYLOAD_FORMAT = (f'< {p.AUTHENTICATOR_IV_SIZE}s {p.AES_CBC_BLOCK_SIZE}s {p.AES_CBC_BLOCK_SIZE}s '
                               f'{p.AES_CBC_BLOCK_SIZE}s {p.AES_CBC_BLOCK_SIZE}s {p.VERSION_SIZE}s {p.CLIENT_ID_SIZE}s '
                               f'{p.SERVER_ID_SIZE}s {p.TICKET_IV_SIZE}s {p.CREATION_TIME_SIZE}s  {p.TICKET_IV_SIZE}s '
                               f'{2 * p.AES_CBC_BLOCK_SIZE}s {p.AES_CBC_BLOCK_SIZE}s')

    @staticmethod
    def parse(data):
        try:
            (authenticator_iv, authenticator_version, authenticator_client_id, authenticator_server_id,
             authenticator_creation_time, ticket_version, ticket_client_id, ticket_server_id, ticket_creation_time,
             ticket_iv, ticket_aes_key, ticket_expiration_time) = struct.unpack(
                SymKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
            decrypted_ticket = DecryptedTicket(ticket_version, ticket_client_id, ticket_server_id, ticket_creation_time,
                                               ticket_iv, ticket_aes_key, ticket_expiration_time)
            decrypt_authenticator = DecryptedAuthenticator(decrypted_ticket.decrypted_client_and_msg_server_aes_key,
                                                           authenticator_iv, authenticator_version,
                                                           authenticator_client_id,
                                                           authenticator_server_id, authenticator_creation_time)
            payload = p.RequestAuthenticatorAndTicketPayload(decrypt_authenticator,
                                                             decrypted_ticket)

            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing payload in msg server')


class MsgPayloadParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< I'

    @staticmethod
    def parse(data):
        try:
            message_size = struct.unpack(MsgPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data[:p.MESSAGE_SIZE_SIZE])[0]
            # we want to calculate the message size after encryption
            new_protocol_payload_format = f'< {p.MESSAGE_IV_SIZE}s {message_size}s'
            message_iv, message_content = struct.unpack(new_protocol_payload_format, data[p.MESSAGE_SIZE_SIZE:])
            payload = p.RequestSendMsgPayload(message_size, message_iv, message_content)
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error while getting the message size')
