import base64
import datetime
import socket
import unittest
from unittest.mock import patch, mock_open
from Crypto.Cipher import AES
import struct


def func():
    with open('text.txt', 'w') as f:
        f.write('Hello world!')


class Test(unittest.TestCase):

    def test_ip(self):
        time = str(datetime.datetime.now().timestamp()).encode('utf-8')
        packed = struct.pack(f'{len(time)}s', time)
        print(base64.b64encode(packed))
        print(packed)
        print(time)
        byte_string = 'Yq\\x15f\\x00\\x00\\x00\\x00'
        print(byte_string.decode('utf-8'))

        # Extract the hexadecimal string (excluding 'b' and single quotes)
        hex_string = ''.join(char for char in byte_string[1:] if char in '0123456789abcdefABCDEF')
        print(float.fromhex(hex_string))

        # Convert the hexadecimal string to an integer
        int_value = float(bytes.fromhex(hex_string))

        # Interpret the integer as a float
        # float_value = struct.unpack('d', int_value.to_bytes(8, 'little'))[0]

        print(int_value)


        # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # s1.connect(('8.8.8.0', 80))
        # s.connect(('8.8.8.8', 800))
        # ip1 = s1.getsockname()[0]
        # ip = s.getsockname()[0]
        # print(ip + "\n" + ip1)
        # s.close()
        # print(AES.block_size)

    @patch('builtins.open', newcallable=mock_open)
    def testif_file_open(self, mock_open_file):
        func()
        mock_open_file.assert_called_once_with('text.txt', 'w')

    def test_if_data_write(self):
        with patch('builtins.open', new_callable=mock_open) as mock_open_file:
            func()
            f = mock_open_file()
            f.write.assert_called_once_with('Hello world!')
