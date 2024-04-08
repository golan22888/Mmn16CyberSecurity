import os
import uuid

ME_INFO_PATH = 'me.info'


def read_client_info_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) == 2:
                client_name = lines[0].strip()
                client_id = lines[1].strip()
                return True, client_name, client_id
    except FileNotFoundError:
        print('Could not find me.info in the specified directory.')
    return False, None, None


def get_client_info():
    if os.path.exists(ME_INFO_PATH):
        success, client_name, client_id = read_client_info_from_file(ME_INFO_PATH)
        if success:
            print("Welcome back, {}! Your client ID is {}.".format(client_name, client_id))
            return True, client_name, uuid.UUID(client_id)
        else:
            print('could not read me.info')
            return False, None, None
    else:
        print('me.info not found in {}'.format(ME_INFO_PATH))
        return False, None, None


def add_to_me_info(client_name, client_id):
    try:
        with open(ME_INFO_PATH, 'w') as file:
            file.write(f"{client_name}\n{client_id}")
    except FileNotFoundError:
        print('Could not find me.info in the specified directory.')
