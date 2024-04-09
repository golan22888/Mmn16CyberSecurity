import uuid
from threading import Lock
from client import Client

CLIENT_FILE_PATH = './clients.txt'


class ClientsManager:
    def __init__(self):
        self.lock = Lock()
        self.clients = []
        self.load_clients()

    def load_clients(self):
        try:
            with open(CLIENT_FILE_PATH, 'r') as file:
                for line in file:
                    client_data = line.strip().split(":")
                    client = Client(uuid.UUID(hex=client_data[0]), client_data[1], client_data[2])
                    self.clients.append(client)
        except FileNotFoundError:
            print("File not found")

    def save_client(self, client):
        if client.get_client_id() in self.clients:
            self.update_key_validity(client)
        else:
            with open(CLIENT_FILE_PATH, "a") as file:
                self.clients.append(client)
                file.write(
                    f"{client.get_client_id()}:{client.get_client_msg_server_key()}:{client.get_expiration_time()}\n")

    def get_client_by_id(self, client_id):
        with self.lock:
            for client in self.clients:
                if client.get_client_id() == client_id:
                    return client

    def update_key_validity(self, client):
        try:
            client_index = self.get_client_index_by_id(client.get_client_id())
            self.clients[client_index].set_expiration_time(client.get_expiration_time())
            self.clients[client_index].set_client_msg_server_key(client.get_client_msg_server_key())
            self.update_client_in_file(client_index, client)
        except Exception as e:
            print(e)
            print('Error updating last seen')

    def get_client_index_by_id(self, client_id):
        with self.lock:
            for index, client in enumerate(self.clients):
                if client.get_client_id() == client_id:
                    return index
            return -1

    def update_client_in_file(self, line_index, client):
        with self.lock:
            try:
                with open(CLIENT_FILE_PATH, 'r+') as file:

                    lines = file.readlines()

                    if 0 <= line_index < len(lines):
                        client_info = lines[line_index].strip().split(':')
                        if len(client_info) == 3:
                            client_info[1] = client.get_client_msg_server_key()
                            client_info[2] = client.get_expiration_time()
                            lines[line_index] = ':'.join(client_info) + '/n'

                            file.seek(0)
                            file.writelines(lines)
                            file.truncate()
            except Exception as e:
                print(e)
                print('Error updating last seen in the file')
