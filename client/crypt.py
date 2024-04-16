import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import uuid


def encrypt_aes_cbc(key, plaintext, iv):
    if iv is None:
        iv = get_random_bytes(AES.block_size)
    else:
        iv = base64.b64decode(iv)
    if isinstance(plaintext, uuid.UUID):
        plaintext = plaintext.bytes
    elif isinstance(plaintext, int):
        plaintext = plaintext.to_bytes(1, byteorder="little")  # Convert integer to bytes
    elif isinstance(plaintext, bytes):
        pass  # Do nothing if plaintext is already bytes
    else:
        plaintext = plaintext.encode('utf-8')  # Convert string to bytes
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext, AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext), base64.b64encode(iv)


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
