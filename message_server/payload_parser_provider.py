import op


class PayloadParserProvider:
    @staticmethod
    def get_payload_parser(code):
        parser = op.OPS.get(code).get('parser')
        return parser
