from abc import ABC, abstractmethod
import struct
import payload as p


class PayloadParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(data):
        pass


class SymKeyPayloadParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< {p.AUTHENTICATOR_SIZE}s {p.TICKET_SIZE}s'

    @staticmethod
    def parse(data):
        try:
            authenticator, ticket = struct.unpack(SymKeyPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data)
            payload = p.RequestAuthenticatorAndTicketPayload(authenticator.rstrip(b'\x00').decode('utf-8'),
                                                             ticket.rstrip(b'\x00').decode('utf-8'))

            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing payload in msg server')


class MsgPayloadParser(PayloadParser):
    PROTOCOL_PAYLOAD_FORMAT = f'< I'

    @staticmethod
    def parse(data):
        try:
            message_size = struct.unpack(MsgPayloadParser.PROTOCOL_PAYLOAD_FORMAT, data[:p.MESSAGE_SIZE_SIZE])
            new_protocol_payload_format = f'< {p.MESSAGE_IV_SIZE}s {message_size}s'
            message_iv, message_content = struct.unpack(new_protocol_payload_format, data[p.MESSAGE_SIZE_SIZE:])
            payload = p.RequestSendMsgPayload(message_size, message_iv, message_content)
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error while getting the message size')


