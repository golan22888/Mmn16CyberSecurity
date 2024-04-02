from header import ResponseHeader
import payload as p
from message import Message
from crypt import decrypt_aes_cbc as decrypt

SERVER_VERSION = 24


class ResponseProvider:
    @staticmethod
    def make_response(request, code):
        match code:
            case 1605 | 1609:
                payload = p.ResponseEmptyPayload()
            case 1604:
                payload = p.ResponseEmptyPayload()
            case default:
                raise ValueError(f'Unknown response code: {code}')

        header = ResponseHeader(SERVER_VERSION, code)
        response = Message(header, payload)

        return response


