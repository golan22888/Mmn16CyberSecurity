from header import ResponseHeader
import payload as p
from message import Message
from message_server_constant import SERVER_VERSION


class ResponseProvider:
    @staticmethod
    def make_response(request, code):
        match code:
            case 1609:
                payload = p.ResponseEmptyPayload()
            case 1604 | 1605:
                payload = p.ResponseEmptyPayload()
                print(f"response {code} is being sent")
            case default:
                raise ValueError(f'Unknown response code: {code}')

        header = ResponseHeader(SERVER_VERSION, code)
        response = Message(header, payload)

        return response
