from header_parser import HeaderParser
from payload_parser_provider import PayloadParserProvider


class RequestParser:
    @staticmethod
    def parse_header(data):
        try:
            header = HeaderParser.parse(data)
            return header
        except Exception as e:
            print(e)
            raise Exception('Error parsing header in Message Server')

    @staticmethod
    def parse_payload(code, data):
        try:
            payload_parser = PayloadParserProvider.get_payload_parser(code)
            payload = payload_parser.parse(data)
            return payload
        except Exception as e:
            print(e)
            raise Exception('Error parsing payload in Message Server')

