import base64
from abc import ABC
from crypt import encrypt_aes_cbc as encrypt


class Payload(ABC):
    pass


class SendNameAndPassPayload(Payload):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password


class SendServerIdAndNoncePayload(Payload):
    def __init__(self, server_id, nonce):
        self.serverId = server_id
        self.nonce = nonce

    def get_server_id(self):
        return self.serverId

    def get_nonce(self):
        return self.nonce


class SendAuthenticatorAndTicketPayload(Payload):
    def __init__(self, authenticator, ticket):
        self.authenticator = authenticator
        self.ticket = ticket

    def get_authenticator(self):
        return self.authenticator

    def get_ticket(self):
        return self.ticket


class SendMessagePayload(Payload):
    def __init__(self, message_content, key):
        self.message_content, self.message_iv = encrypt(key, message_content, None)
        self.message_size = len(base64.b64decode(self.message_content))

    def get_message_size(self):
        return self.message_size

    def get_message_iv(self):
        return self.message_iv

    def get_message_content(self):
        return base64.b64decode(self.message_content)


class ReceiveRegistrationSucceededPayload(Payload):
    def __init__(self, client_id):
        self.client_id = client_id

    def get_client_id(self):
        return self.client_id


class ReceiveSymKeyAndTicketPayload(Payload):
    def __init__(self, client_id, decrypted_key, ticket):
        self.client_id = client_id
        self.decrypted_key = decrypted_key
        self.ticket = ticket

    def get_client_id(self):
        return self.client_id

    def get_decrypted_key(self):
        return self.decrypted_key

    def get_ticket(self):
        return self.ticket


class EmptyPayload(Payload):
    def __init__(self):
        self.size = 0
