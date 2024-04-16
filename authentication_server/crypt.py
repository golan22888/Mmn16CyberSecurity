import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import datetime
import struct
from authenticator_constant import AES_KEY_SIZE


def generate_aes_key():
    aes_key = get_random_bytes(AES_KEY_SIZE)
    return aes_key


def encrypt_aes_cbc(key, plaintext, iv):
    if iv is None:
        iv = get_random_bytes(AES.block_size)
    else:
        iv = base64.b64decode(iv)
    if isinstance(plaintext, datetime.datetime):
        # Convert datetime to string representation
        datetime_str = plaintext.strftime('%Y-%m-%d %H:%M:%S')
        # Encode the string to bytes using UTF-8 encoding
        plaintext = datetime_str.encode('utf-8')
    elif isinstance(plaintext, int):
        plaintext = str(plaintext).encode('utf-8')  # Convert integer to bytes
    elif isinstance(plaintext, float):
        plaintext = struct.pack('d', plaintext)  # Convert float to bytes
    elif isinstance(plaintext, bytes):
        pass  # Do nothing if plaintext is already bytes
    else:
        plaintext = plaintext.encode('utf-8')  # Convert string to bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext), base64.b64encode(iv)
