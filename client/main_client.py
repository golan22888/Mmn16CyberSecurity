from me import get_client_info
from srv import get_servers_info
from connection import Connection


if __name__ == "__main__":
    auth_server_ip, auth_server_port, msg_server_ip, msg_server_port = get_servers_info()
    connection = Connection(auth_server_ip, auth_server_port)
    connection.connect()

    success, client_name, client_id = get_client_info()
    if not success:
        username = input("Enter your username: ")
        password = input("Enter your password: ")


