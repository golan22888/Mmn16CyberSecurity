import payload_parser
import payload_serializer


OPS = {
    # REQUEST
    1024:
        {
            'serializer': payload_serializer.RegistrationPayloadSerializer
        },
    1027:
        {
            'serializer': payload_serializer.AuthenticationPayloadSerializer
        },
    1028:
        {
            'serializer': payload_serializer.AuthenticatorAndTicketPayloadSerializer
        },
    1029:
        {
            'serializer': payload_serializer.MsgPayloadSerializer
        },
    # RESPONSE
    1600:
        {
            'parser': payload_parser.RegistrationSucceededParser
        },
    1603:
        {
            'parser': payload_parser.SymKeyAndTicketParser
        }
}
