from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

AES_KEY_SIZE = 32


def decrypt_aes_cbc(key, ciphertext, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
        decrypted_data = cipher.decrypt(base64.b64decode(ciphertext))
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data.decode('utf-8')
    except Exception as e:
        print("Error decrypting data:", e)
        return None
