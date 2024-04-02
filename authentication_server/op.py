import payload_parser

import payload_serializer
import handler

OPS = {
    # REQUESTS
    1024: {
        'parser': payload_parser.RegisterPayloadParser,
        'handler': handler.RegisterHandler
    },
    1027: {
        'parser': payload_parser.RequestSymKeyPayloadParser,
        'handler': handler.SymKeyRequestHandler
    },
    # RESPONSE
    1600: {
        'serializer': payload_serializer.RegisterPayloadSerializer
    },
    1601: {
        'serializer': payload_serializer.EmptyPayloadSerializer
    },
    1603: {
        'serializer': payload_serializer.RequestSymKeyPayloadSerializer
    },
    1609: {
        'serializer': payload_serializer.EmptyPayloadSerializer
    }
}
