from port import get_port
from server import Server
from clients_manager import ClientsManager

if __name__ == "__main__":
    try:
        port = get_port()
        client_manager = ClientsManager()

        server = Server(port, client_manager)
        server.start()
    except Exception as e:
        print(e)
