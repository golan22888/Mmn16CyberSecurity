import ast

MSG_INFO_PATH = '../associated_files/msg.info'


def get_key_from_file():
    try:
        with open(MSG_INFO_PATH, 'r') as file:
            servers_mutual_key = file.readlines()[3]
            return ast.literal_eval(servers_mutual_key)
    except FileNotFoundError:
        print(f'{MSG_INFO_PATH} file not found.')
