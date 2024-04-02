import socket
import unittest
from unittest.mock import patch, mock_open
from Crypto.Cipher import AES


def func():
    with open('text.txt', 'w') as f:
        f.write('Hello world!')


class Test(unittest.TestCase):

    def test_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s1.connect(('8.8.8.0', 80))
        s.connect(('8.8.8.8', 800))
        ip1 = s1.getsockname()[0]
        ip = s.getsockname()[0]
        print(ip + "\n" + ip1)
        s.close()
        print(AES.block_size)

    @patch('builtins.open', newcallable=mock_open)
    def testif_file_open(self, mock_open_file):
        func()
        mock_open_file.assert_called_once_with('text.txt', 'w')

    def test_if_data_write(self):
        with patch('builtins.open', new_callable=mock_open) as mock_open_file:
            func()
            f = mock_open_file()
            f.write.assert_called_once_with('Hello world!')
