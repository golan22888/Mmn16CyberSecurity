from abc import ABC


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
