import argparse
import logging
import json
from TripleDES_symmetric import TripleDES
from RSA_asymmetric import RSA
from read_and_write_file import load_settings, write_symmetric_key, load_symmetric_key, write_asymmetric_key, load_private_key,  write_file, load_text
SETTING_FILE='settings.json'
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-set', '--settings', default=SETTING_FILE, type=str,help='Allows you to use your own json file with paths"(Enter the path to the file)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen','--generation',action='store_true',help='Запускает режим генерации ключей')
    group.add_argument('-enc','--encryption',action='store_true',help='Запускает режим шифрования')
    group.add_argument('-dec','--decryption',action='store_true',help='Запускает режим дешифрования')
    args=parser.parse_args()
    settings=load_settings(args.settings)
    triple_des=TripleDES(settings['symmetric_key'])
    rsa=RSA(settings['private_key'],settings['public_key'])
    if settings:
        match True:
            case args.generation:
                logging.info('The key generation mode starts')
                length=triple_des.ask_user_length_key()
                sym_key=triple_des.generate_3des_key(length)
                private_key, public_key=rsa.generate_rsa_key()
                cipher_sym_key=rsa.encrypt_rsa(public_key,sym_key)
                write_asymmetric_key(private_key, public_key, settings['private_key'], settings['public_key'])
                write_symmetric_key(cipher_sym_key, settings['symmetric_key'])
            case args.encryption:
                logging.info('Encryption mode begins.')
                private_key=load_private_key(settings['private_key'])
                cipher_key=load_symmetric_key(settings['symmetric_key'])
                symmectric_key=rsa.decrypt_rsa(private_key, cipher_key)
                text=load_text(settings['initial_file'])
                cipher_text=triple_des.encrypt_3des(symmectric_key, text)
                write_file(settings['encrypted_file'], cipher_text)
            case args.decryption:
                logging.info('Decryption mode begins.')
                private_key=load_private_key(settings['private_key'])
                cipher_key=load_symmetric_key(settings['symmetric_key'])
                symmetric_key=rsa.decrypt_rsa(private_key,cipher_key)
                cipher_text=load_text(settings['encrypted_file'])
                text=triple_des.decrypt_3des(symmetric_key,cipher_text)
                write_file(settings['decrypted_file'], text)