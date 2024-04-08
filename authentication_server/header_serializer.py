import struct

PROTOCOL_HEADER_FORMAT = '< B H I'


class HeaderSerializer:
    @staticmethod
    def serialize(header):
        try:
            version = header.get_version()
            code = header.get_code()
            payload_size = header.get_payload_size()

            serialized_header = struct.pack(PROTOCOL_HEADER_FORMAT, version, code, payload_size)
        except Exception as e:
            raise Exception('Error occurred while serializing header in auth')

        return serialized_header
