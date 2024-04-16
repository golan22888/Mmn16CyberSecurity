import uuid
from abc import ABC, abstractmethod
import struct
import base64
import client_constant as c


class PayloadSerializer(ABC):
    @staticmethod
    @abstractmethod
    def serialize(payload):
        pass


# requests to the authentication server
class RegistrationPayloadSerializer(PayloadSerializer):
    PROTOCOL_PAYLOAD_FORMAT = f'< {c.NAME_SIZE}s {c.PASSWORD_SIZE}s'

    @staticmethod
    def serialize(payload):
        name = payload.get_name().encode('utf-8')
        password = payload.get_password().encode('utf-8')
        serialized_payload = struct.pack(RegistrationPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT, name, password)
        return serialized_payload


class AuthenticationPayloadSerializer(PayloadSerializer):
    PROTOCOL_PAYLOAD_FORMAT = f'< {c.SERVER_ID_SIZE}s {c.NONCE_SIZE}s'

    @staticmethod
    def serialize(payload):
        server_id = uuid.UUID(hex=payload.get_server_id())
        nonce = payload.get_nonce()
        serialized_payload = struct.pack(AuthenticationPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT,
                                         server_id.bytes, nonce)

        return serialized_payload


# requests to the message server
class AuthenticatorAndTicketPayloadSerializer(PayloadSerializer):
    # version, client_id, server_id, creation_time, aes_key, expiration_time -> those arguments are encrypted, so we
    # need to get them with their padding
    PROTOCOL_PAYLOAD_FORMAT = (
        f'< {c.AUTHENTICATOR_IV_SIZE}s {c.AES_CBC_BLOCK_SIZE}s {2 * c.AES_CBC_BLOCK_SIZE}s {2 * c.AES_CBC_BLOCK_SIZE}s '
        f'{c.AES_CBC_BLOCK_SIZE}s ')

    @staticmethod
    def serialize(payload):
        authenticator = payload.get_authenticator()
        ticket = payload.get_ticket()
        serialized_payload = struct.pack(AuthenticatorAndTicketPayloadSerializer.PROTOCOL_PAYLOAD_FORMAT,
                                         base64.b64decode(authenticator.get_authenticator_iv()),
                                         base64.b64decode(authenticator.get_version()),
                                         base64.b64decode(authenticator.get_client_id()),
                                         base64.b64decode(authenticator.get_server_id()),
                                         base64.b64decode(authenticator.get_creation_time()))

        return serialized_payload + ticket


class MsgPayloadSerializer(PayloadSerializer):
    @staticmethod
    def serialize(payload):
        message_size = payload.get_message_size()
        message_iv = payload.get_message_iv()
        message_iv = base64.b64decode(message_iv)
        message_content = payload.get_message_content()
        protocol_payload_format = f'< I {c.MESSAGE_IV_SIZE}s {message_size}s'

        serialized_payload = struct.pack(protocol_payload_format, message_size, message_iv,
                                         message_content)

        return serialized_payload
