import json
import os


class PersistentDataStorage:
    def __init__(self):
        base_dir = os.path.expanduser('~/.config/chitchat')
        os.makedirs(base_dir, exist_ok=True)
        data_dir = os.path.join(base_dir, 'chitchat_data')
        os.makedirs(data_dir, exist_ok=True)
        secret_file = os.path.join(data_dir, 'secret.txt')
        self.filename = 'chitchat1.txt'
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}
            with open(self.filename, 'w') as f:
                json.dump(self.data, f)

    def store(self, key, value):
        self.data[key] = value
        with open(self.filename, 'w') as f:
            json.dump(self.data, f)

    def retrieve(self, key):
        return self.data.get(key, None)


storage = PersistentDataStorage()
