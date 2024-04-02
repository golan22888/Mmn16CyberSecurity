from abc import ABC

VERSION_SIZE = 1
MESSAGE_SIZE_SIZE = 4
NONCE_SIZE = 8
EXPIRATION_TIME_SIZE = CREATION_TIME_SIZE = 8
CLIENT_ID_SIZE = SERVER_ID_SIZE = 16
ENCRYPTED_KEY_IV_SIZE = TICKET_IV_SIZE = AUTHENTICATOR_IV_SIZE = MESSAGE_IV_SIZE = 16
AES_KEY_SIZE = 32
CLIENT_NAME_SIZE = CLIENT_PASSWORD_SIZE = 255
TICKET_SIZE = (VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE + TICKET_IV_SIZE + AES_KEY_SIZE +
               EXPIRATION_TIME_SIZE)
AUTHENTICATOR_SIZE = AUTHENTICATOR_IV_SIZE + VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE


class Payload(ABC):
    pass


class RequestOfNameAndPassPayload(Payload):
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    @staticmethod
    def get_size():
        return CLIENT_NAME_SIZE + CLIENT_PASSWORD_SIZE


class RequestOfServerIdAndNoncePayload(Payload):
    def __init__(self, server_id, nonce):
        self.serverId = server_id
        self.nonce = nonce

    def get_server_id(self):
        return self.serverId

    def get_nonce(self):
        return self.nonce

    @staticmethod
    def get_size():
        return SERVER_ID_SIZE + NONCE_SIZE


class RequestOfAuthenticatorAndTicketPayload(Payload):
    def __init__(self, authenticator, ticket):
        self.authenticator = authenticator
        self.ticket = ticket

    def get_authenticator(self):
        return self.authenticator

    def get_ticket(self):
        return self.ticket

    @staticmethod
    def get_size():
        return TICKET_SIZE + AUTHENTICATOR_SIZE


class RequestOfMessagePayload(Payload):
    def __init__(self, message_size, message_iv, message_content):
        self.message_size = message_size
        self.message_iv = message_iv
        self.message_content = message_content

    def get_message_size(self):
        return self.message_size

    def get_message_iv(self):
        return self.message_iv

    def get_message_content(self):
        return self.message_content

    def get_size(self):
        return MESSAGE_SIZE_SIZE + MESSAGE_IV_SIZE + self.message_size


class ResponseToRegistrationSucceededPayload(Payload):
    def __init__(self, client_id):
        self.client_id = client_id

    def get_client_id(self):
        return self.client_id


class ResponseToSymKeyAndTicketPayload(Payload):
    def __init__(self, client_id, encrypted_key, ticket):
        self.client_id = client_id
        self.encrypted_key = encrypted_key
        self.ticket = ticket

    def get_client_id(self):
        return self.client_id

    def get_encrypted_key(self):
        return self.encrypted_key

    def get_ticket(self):
        return self.ticket

# class ResponseToEmtpyPayload(Payload):
