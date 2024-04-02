
class Client:
    def __init__(self, client_id, name, password_hash, last_seen):
        self.client_id = client_id
        self.name = name
        self.password_hash = password_hash
        self.last_seen = last_seen

    def get_client_id(self): return self.client_id
    def get_name(self): return self.name
    def get_password_hash(self): return self.password_hash
    def get_last_seen(self): return self.last_seen
    def set_last_seen(self, last_seen): self.last_seen = last_seen
