from header_serializer import HeaderSerializer
from payload_serializer_provider import PayloadSerializerProvider


class ResponseSerializer:
    @staticmethod
    def serialize_header(header):
        try:
            serialized_header = HeaderSerializer.serialize(header)
            return serialized_header
        except Exception as e:
            print(e)
            raise Exception("Error occurred while serializing header")

    @staticmethod
    def serialize_payload(code, payload):
        try:
            payload_serializer = PayloadSerializerProvider.get_payload_serializer(code)
            serialized_payload = payload_serializer.serialize(payload)
            return serialized_payload
        except Exception as e:
            print(e)
            raise Exception("Error occurred while serializing payload")

    @staticmethod
    def serialize(response):
        try:
            serialized_payload = ResponseSerializer.serialize_payload(response.get_header().get_code(),
                                                                      response.get_payload())
            response.header.payload_size = len(serialized_payload)
            serialized_header = ResponseSerializer.serialize_header(response.header)
            if response.get_header().get_code() == 1603:
                ResponseSerializer.print_to_catch_packet(serialized_header + serialized_payload)
            return serialized_header + serialized_payload
        except Exception as e:
            print(e)
            raise Exception("Error occurred while serializing response")

    @staticmethod
    def print_to_catch_packet(response):
        with open("../offline_attack/packet_1603", "w") as file:
            # Write some content to the file
            print(response, file=file)
