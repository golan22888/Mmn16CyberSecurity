import payload_parser
import payload_serializer
import handler


OPS = {
    # REQUEST
    1024:
        {
            'serializer': payload_serializer.NameAndPassSerializer
        },
    1027:
        {
            'serializer': payload_serializer.ServerIdAndNonceSerializer
        },
    1028:
        {
            'serializer': payload_serializer.AuthenticatorAndTicketSerializer
        },
    1029:
        {
            'serializer': payload_serializer.MessageSerializer
        },
    # RESPONSE
    1600:
        {
            'parser': payload_parser.RegistrationSucceededParser,
            'handler': handler.RegistrationSucceededHandler
        },
    1601:
        {
            'parser': payload_parser.RegistrationFailedParser,
            'handler': handler.RegistrationFailedHadler
        },
    1603:
        {
            'parser': payload_parser.RecieveSymKeyParser,
            'handler': handler.RecieveSymKeyHandler
        },
    1604:
        {
          'parser': payload_parser.SymKeyAcceptedParser,
          'handler': handler.SymKeyAcceptedHandler
        },
    1605:
        {
            'parser': payload_parser.MsgAcceptedParser,
            'handler': handler.MsgAcceptedHandler
        },
    1609:
        {
            'parser': payload_parser.GeneralErrorParser,
            'handler': handler.GeneralErrorHandler
        }
}