import base64
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
        if not self.get_client_by_id(client.get_client_id()):
            self.clients.append(client)
            with open(CLIENT_FILE_PATH, "a") as file:
                print(
                    f"{client.get_client_id()}:{base64.b64encode(client.get_client_msg_server_key())}:{client.get_expiration_time()}",
                    file=file)
        else:
            for index, client_in_memory in enumerate(self.clients):
                if client_in_memory.get_client_id() == client.get_client_id():
                    client_in_memory.set_client_msg_server_key(client.get_client_msg_server_key())
                    client_in_memory.set_expiration_time(client.get_expiration_time())
                    self.update_clients_in_file(index, client_in_memory)
                    break

    def get_client_by_id(self, client_id):
        with self.lock:
            for client in self.clients:
                if client.get_client_id() == client_id:
                    return client
            return False

    def update_key_validity(self, client):
        try:
            client_index = self.get_client_index_by_id(client.get_client_id())
            self.clients[client_index].set_expiration_time(client.get_expiration_time())
            self.clients[client_index].set_client_msg_server_key(client.get_client_msg_server_key())
            self.update_clients_in_file(client_index, client)
        except Exception as e:
            print(e)
            print('Error updating last seen')

    def get_client_index_by_id(self, client_id):
        with self.lock:
            for index, client in enumerate(self.clients):
                if client.get_client_id() == client_id:
                    return index
            return -1

    def update_clients_in_file(self, line_index, client):
        with self.lock:
            try:
                with open(CLIENT_FILE_PATH, 'r+') as file:

                    lines = file.readlines()
                    if client is None:
                        pass
                    elif 0 <= line_index < len(lines):
                        client_info = lines[line_index].strip().split(':')
                        if len(client_info) == 3:
                            client_info[1] = str(base64.b64encode(client.get_client_msg_server_key()))
                            client_info[2] = str(client.get_expiration_time())
                            lines[line_index] = ':'.join(client_info) + '\n'

                            file.seek(0)
                            file.writelines(lines)
                            file.truncate()
            except Exception as e:
                print(e)
                print('Error updating last seen in the file')
