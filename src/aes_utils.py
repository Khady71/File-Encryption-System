from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import sys

BUFFER_SIZE = 1024 * 1024  


def encrypt_file(input_path, key):
    file_in = open(input_path, 'rb')
    output_path = input_path + '.encrypted'
    file_out = open(output_path, 'wb')
    aesgcm = AESGCM(key)

    while chunk := file_in.read(BUFFER_SIZE):
        nonce = os.urandom(12)
        encrypted_chunk = aesgcm.encrypt(nonce, chunk, None)
        file_out.write(len(nonce+encrypted_chunk).to_bytes(4, "big"))
        file_out.write(nonce+encrypted_chunk)
        chunk = file_in.read(BUFFER_SIZE)

    file_in.close()   
    file_out.close()




def decrypt_file(input_path, key):
    file_in = open(input_path, 'rb')
    output_filename = input_path.replace('.encrypted', '.decrypted')
    file_out = open(output_filename, 'wb')
    aesgcm = AESGCM(key)

    while size_bytes := file_in.read(4):
        chunk_size = int.from_bytes(size_bytes, "big")
        chunk = file_in.read(chunk_size)
        nonce = chunk[:12]
        ciphertext = chunk[12:]
        decrypted_chunk = aesgcm.decrypt(nonce, ciphertext, None)
        file_out.write(decrypted_chunk)

    file_in.close()
    file_out.close()

script_dir = os.path.dirname(os.path.abspath(__file__))
# input_filename = os.path.join(script_dir, 'test_input.txt')
# input_filename = os.path.join(script_dir, 'test.pdf')

# encrypted_filename = os.path.join(script_dir, 'test_input.txt.encrypted')
encrypted_filename = os.path.join(script_dir, 'test.pdf.encrypted')


# key = AESGCM.generate_key(bit_length=256)
hex_key = "2d24441dce98e670dbe99c24bdd10140a98f78843e0441e94f513ce9230801b2"
key_bytes = bytes.fromhex(hex_key)

# encrypt_file(input_filename,key_bytes)
decrypt_file(encrypted_filename, key_bytes)