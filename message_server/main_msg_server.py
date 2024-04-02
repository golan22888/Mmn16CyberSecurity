from server import Server
from read_from_msg_info import get_port_server_mutual_key as data

from clients_manager import ClientsManager


SERVER_VERSION = 24

if __name__ == "__main__":
    try:
        port, server_id, mutual_key = data()
        clients_manager = ClientsManager()

        server = Server(port, clients_manager)
        server.start()
    except Exception as e:
        print(e)
