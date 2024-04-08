import struct

from header import RequestHeader

PROTOCOL_HEADER_FORMAT = f'< B H I'
HEADER_SIZE = struct.calcsize(PROTOCOL_HEADER_FORMAT)


class HeaderParser:
    @staticmethod
    def parse(data):
        try:
            version, code, payload_size = struct.unpack(PROTOCOL_HEADER_FORMAT, data[:HEADER_SIZE])
            header = RequestHeader(version, code, payload_size)
        except Exception as e:
            raise Exception('Error parsing header')

        return header
