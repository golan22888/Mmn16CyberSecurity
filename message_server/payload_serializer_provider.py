import op


class PayloadSerializerProvider:
    @staticmethod
    def get_payload_serializer(code):
        serializer = op.OPS.get(code).get('serializer')
        return serializer
