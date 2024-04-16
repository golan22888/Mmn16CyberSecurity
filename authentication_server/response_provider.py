from header import ResponseHeader
import payload as p
from message import Message
from authenticator_constant import SERVER_VERSION


class ResponseProvider:
    @staticmethod
    def make_response(request, code, **data):
        match code:
            case 1600:
                payload = p.ResponsePayload(data.get("client_id"))

                print(f'response: {code} is being made for client {data.get("client_id")}\n')
            case 1601 | 1609:
                payload = p.ResponseEmptyPayload()
            case 1603:
                payload = p.ResponseKeyPayload(
                    data.get("client_id"),
                    data.get("encrypted_key"),
                    data.get("ticket")
                )
            case default:
                raise ValueError(f'Unknown response code: {code}')

        header = ResponseHeader(SERVER_VERSION, code)
        response = Message(header, payload)

        return response
