import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class TripleDES:
    def __init__(self, symmetric_key_path: str) -> None:
        self.symmetric_key = symmetric_key_path

    def encrypt_3des(self, key: bytes, plaintext: bytes) -> bytes:
        padder = padding.PKCS7(algorithms.TripleDES.block_size).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        cipher = Cipher(
            algorithms.TripleDES(key),
            modes.ECB(),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return ciphertext

    def decrypt_3des(self, key: bytes, ciphertext: bytes) -> bytes:
        cipher = Cipher(
            algorithms.TripleDES(key),
            modes.ECB(),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext)+ decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.TripleDES.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext)+ unpadder.finalize()
        return plaintext

    def ask_user_length_key(self) -> int:
        while True:
            try:
                length = int(input("Enter key length (64, 128, or 192): "))
                if length in [64, 128, 192]:
                    return length
                else:
                    raise ValueError("Please enter 64, 128, or 192.")
            except ValueError as e:
                print("Invalid input.")

    def generate_3des_key(self, length: int) -> bytes:
        return os.urandom(length//8)