import struct
from header import RequestHeader, CLIENT_ID_SIZE
import uuid

PROTOCOL_HEADER_FORMAT = f'< {CLIENT_ID_SIZE}s B H I'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)


class HeaderParser:
    @staticmethod
    def parse(data):
        try:
            client_id, version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, data[:HEADER_SIZE])
            header = RequestHeader(uuid.UUID(bytes=client_id), version, code, payload_size)
        except Exception as e:
            raise Exception('Error parsing header')

        return header
