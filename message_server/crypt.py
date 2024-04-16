from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt_aes_cbc(key, ciphertext, iv):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        unpadded_data = unpad(decrypted_data, AES.block_size)
        return unpadded_data
    except Exception as e:
        print("Error decrypting data:", e)
        return None
