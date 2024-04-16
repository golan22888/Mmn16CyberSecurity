import struct
from client_constant import CLIENT_ID_SIZE

PROTOCOL_HEADER_FORMAT = f'< {CLIENT_ID_SIZE}s B H I'


class HeaderSerializer:
    @staticmethod
    def serialize(header):
        try:
            client_id = header.get_client_id().bytes
            code = header.get_code()
            payload_size = header.get_payload_size()
            version = header.get_version()

            serialized_header = struct.pack(PROTOCOL_HEADER_FORMAT, client_id, version, code, payload_size)
        except Exception as e:
            print(e)
            raise Exception('Error occurred while serializing header in client')

        return serialized_header
