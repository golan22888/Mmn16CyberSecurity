import os

SRV_INFO_PATH = 'srv.info'


def read_servers_info_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) == 2:
                auth_server_ip, auth_server_port = lines[0].strip().split(':')
                msg_server_ip, msg_server_port = lines[1].strip().split(':')
                return True, auth_server_ip, auth_server_port, msg_server_ip, msg_server_port
    except FileNotFoundError:
        pass
    return False, None, None


def get_servers_info():
    if os.path.exists(SRV_INFO_PATH):
        success, auth_server_ip, auth_server_port, msg_server_ip, msg_server_port = read_servers_info_from_file(
            SRV_INFO_PATH)
        if success:
            print('succeeded getting servers info from files')
            return auth_server_ip, auth_server_port, msg_server_ip, msg_server_port
        else:
            raise Exception("Invalid format in 'srv.info' file.")
    else:
        raise Exception("File 'srv.info' not found.")
