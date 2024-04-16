import ast
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

FILE = 'packet_'

passwords = []


def get_packet(code):
    try:
        with open(FILE + str(code), 'r') as file:
            packet = file.read()
            return ast.literal_eval(packet)
    except FileNotFoundError:
        print(f'{FILE} file not found. using default port.')
    except ValueError:
        print(f'{FILE} file contains invalid port. Using default port.')
    return -1


def load_passwords(passwords):
    try:
        with open('known_passwords.txt', 'r') as file:
            for line in file:
                password = line.strip()
                passwords.append(password)
    except FileNotFoundError:
        print("File not found")


def decrypt_aes_cbc(key, ciphertext, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data
    except Exception as e:
        print("Error decrypting data:", e)
        return None


def sha256_digest(password):
    password_bytes = password.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(password_bytes)
    digest = sha256_hash.hexdigest()
    return digest


if __name__ == '__main__':
    packet_1027 = get_packet(1027)
    packet_1603 = get_packet(1603)[:55]

    print(packet_1027)
    print(packet_1603)

    iv, encrypted_nonce = struct.unpack(' 23s 16s 16s ', packet_1603)[1:]
    nonce = struct.unpack("39s 8s", packet_1027)[1]
    load_passwords(passwords)
    for password in passwords:
        hash_pass = bytes.fromhex(sha256_digest(password))
        decrypted_nonce = decrypt_aes_cbc(hash_pass, encrypted_nonce, iv)
        if nonce == decrypted_nonce:
            print(password)
            break

