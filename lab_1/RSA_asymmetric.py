import logging

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


logger = logging.getLogger()
logger.setLevel('INFO')


class RSA:
    def __init__(self, private_key_path, public_key_path):
        self.private_key = private_key_path
        self.public_key = public_key_path

    def generate_rsa_key(self) -> tuple:
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = keys
        public_key = keys.public_key()
        logging.info('Asymmetric encryption keys have been generated.')
        return private_key, public_key

    def encrypt_rsa(self, public_key, text: bytes) -> bytes:
        encrypt_text = public_key.encrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                       algorithm=hashes.SHA256(), label=None))
        logging.info('The text is encrypted with an asymmetric encryption algorithm.')
        return encrypt_text

    def decrypt_rsa(self, private_key, text):
        decrypt_text = private_key.decrypt(text, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(), label=None))
        logging.info('The text encrypted with the asymmetric encryption algorithm has been decrypted.')
        return decrypt_text