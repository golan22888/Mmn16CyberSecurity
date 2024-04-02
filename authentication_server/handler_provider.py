import op


class HandlerProvider:
    @staticmethod
    def get_request_handler(code):
        handler = op.OPS.get(code).get('handler')
        return handler
