from abc import ABC

VERSION_SIZE = 1
MESSAGE_SIZE_SIZE = 4
CREATION_TIME_SIZE = EXPIRATION_TIME_SIZE = 8
AUTHENTICATOR_IV_SIZE = TICKET_IV_SIZE = MESSAGE_IV_SIZE = 16
CLIENT_ID_SIZE = SERVER_ID_SIZE = 16
AES_KEY_SIZE = 32
AUTHENTICATOR_SIZE = AUTHENTICATOR_IV_SIZE + VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE
TICKET_SIZE = (VERSION_SIZE + CLIENT_ID_SIZE + SERVER_ID_SIZE + CREATION_TIME_SIZE + TICKET_IV_SIZE + AES_KEY_SIZE +
               EXPIRATION_TIME_SIZE)


class Payload(ABC):
    pass


class RequestAuthenticatorAndTicketPayload(Payload):
    def __init__(self, authenticator, ticket):
        self.authenticator = authenticator
        self.ticket = ticket

    def get_authenticator(self):
        return self.authenticator

    def get_ticket(self):
        return self.ticket


class RequestSendMsgPayload(Payload):
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


class ResponseEmptyPayload(Payload):
    @staticmethod
    def get_size():
        return 0
