import uuid
import hashlib
from threading import Lock
from datetime import datetime
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
                    client = Client(uuid.UUID(hex=client_data[0]), client_data[1], client_data[2], client_data[3])
                    self.clients.append(client)
        except FileNotFoundError:
            print("File not found")

    def save_client(self, client):
        with open(CLIENT_FILE_PATH, "a") as file:
            self.clients.append(client)
            file.write(
                f"{client.get_client_id()}:{client.get_name()}:{client.get_password_hash()}:{client.get_last_seen()}\n")

    def register_client(self, name, password):
        client_id = uuid.uuid4()
        hashed_password = ClientsManager.sha256_digest(password)
        client = Client(client_id, name, hashed_password, datetime.now().timestamp())
        with self.lock:
            self.save_client(client)

    @staticmethod
    def sha256_digest(password):
        password_bytes = password.encode()
        sha256_hash = hashlib.sha256()
        sha256_hash.update(password_bytes)
        digest = sha256_hash.hexdigest()
        return digest

    def update_last_seen_by_id(self, client_id):
        try:
            client_index = self.get_client_index_by_id(client_id)
            last_seen = datetime.now().timestamp()
            self.clients[client_index].set_last_seen(last_seen)
            self.change_last_seen_in_the_file_by_index(client_index, last_seen)
        except Exception as e:
            print(e)
            print('Error updating last seen')

    def get_client_index_by_id(self, client_id):
        with self.lock:
            for index, client in enumerate(self.clients):
                if client.get_client_id() == client_id:
                    return index
            return -1

    def get_client_by_name(self, client_name):
        with self.lock:
            for client in self.clients:
                if client.get_name() == client_name:
                    return client

    def get_client_by_id(self, client_id):
        with self.lock:
            for client in self.clients:
                if client.get_client_id() == client_id:
                    return client

    def change_last_seen_in_the_file_by_index(self, line_index, new_last_seen):
        with self.lock:
            try:
                with open(CLIENT_FILE_PATH, 'r+') as file:

                    lines = file.readlines()

                    if 0 <= line_index < len(lines):
                        client_info = lines[line_index].strip().split(':')
                        if len(client_info) == 4:
                            client_info[3] = new_last_seen
                            lines[line_index] = ':'.join(client_info) + '/n'

                            file.seek(0)
                            file.writelines(lines)
                            file.truncate()
            except Exception as e:
                print(e)
                print('Error updating last seen in the file')
