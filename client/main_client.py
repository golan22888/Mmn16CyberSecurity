
from srv import get_servers_info
from connection import Connection
from client import Client

CLIENT_VERSION = 24

if __name__ == "__main__":
    try:
        auth_server_ip, auth_server_port, msg_server_ip, msg_server_port = get_servers_info()
        client = Client(auth_server_ip, auth_server_port, msg_server_ip, msg_server_port)
        client.start()
    except Exception as e:
        print(e)



