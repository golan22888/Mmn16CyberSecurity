import payload_parser
#
import payload_serializer
import handler

OPS = {
    # REQUESTS
    1028: {
        'parser': payload_parser.SymKeyPayloadParser,
        'handler': handler.SentSymKeyHandler
    },
    1029: {
        'parser': payload_parser.MsgPayloadParser,
        'handler': handler.SentMessageHandler
    },
    # RESPONSE
    1604: {
        'serializer': payload_serializer.EmptyPayloadSerializer
    },
    1605: {
        'serializer': payload_serializer.EmptyPayloadSerializer
    },
    1609: {
        'serializer': payload_serializer.EmptyPayloadSerializer
    }
}
