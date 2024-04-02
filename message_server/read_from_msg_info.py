MSG_INFO_PATH = '../associated_files/msg.info'


def get_port_server_mutual_key():
    try:
        with open(MSG_INFO_PATH, 'r') as file:
            msg_info_lines = file.readlines()
            port = msg_info_lines[0].split(":")[1]
            server_id = msg_info_lines[2]
            servers_mutual_key = msg_info_lines[3]
            return port, server_id, servers_mutual_key
    except FileNotFoundError:
        print(f'{MSG_INFO_PATH} file not found.')
