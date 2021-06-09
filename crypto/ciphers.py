import array
import enum
import os
import random
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.backends import default_backend


class Symbols(enum.Enum):
    DIGITS = "01234567890"
    LOWERCASE = "abcdefghijklmnopqrstuvwxyz"
    UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SYMBOLS = "!@#$%&_*?|"


class SecurePassword:
    def __init__(self):
        self.__symbols = Symbols
        self.__init_values()

    @property
    def symbols(self):
        return self.__symbols

    def __init_values(self):
        self.symbols_seq = str()
        for symbol in self.symbols:
            self.symbols_seq += symbol.value

    @property
    def generate_secure_pass(self):
        password = "".join(random.sample(self.symbols_seq,14 ))
        
        return password


def generate_hash(text):
    text_hash = hashlib.md5()
    text_hash.update(text.encode())

    return text_hash.hexdigest()

def text_decryptor(main_key, secret_text, nonce):
    text_hash = generate_hash(main_key)
    
    algorithm = algorithms.ChaCha20(text_hash.encode(), nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    
    return decryptor.update(secret_text)

def text_encryptor(main_key, secret_message, nonce=None, first=True):
    if not nonce:
        nonce = os.urandom(16)
    key_nonce = main_key
    key_nonce_hash = generate_hash(key_nonce)
    algorithm = algorithms.ChaCha20(key_nonce_hash.encode(), nonce)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    
    if first:
        return encryptor.update(secret_message.encode()), nonce
    else:
        return encryptor.update(secret_message.encode())
