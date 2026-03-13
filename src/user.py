from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair
from ibe_utils import IBEEncryption
from aes_utils import encrypt_file, decrypt_file
import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# _GROUP = PairingGroup('SS512')

class User:
    def __init__(self):

        self.server_url = "http://localhost:8000"
        self.ibe = IBEEncryption('SS512')
        self.group = self.ibe.group
        
        self.P = None
        self.P_pub = None
        self.d_id = None
        self.ID = None
         




    def get_public_params_from_server(self):
        try:
            # print("Just hanging around ")
            response = requests.get(f"{self.server_url}/setup")
            response.raise_for_status()
            data = response.json()
            
            
            # print(f"data['P'] = {data['P']}")  # ← voir le contenu brut
            # print(f"bytes = {bytes.fromhex(data['P'])[:20]}")  
            
            self.P = self.group.deserialize(bytes.fromhex(data['P']))
            
            self.P_pub = self.group.deserialize(bytes.fromhex(data['P_pub']))
            
            print('Got P and P_pub')

            self.ibe.P = self.P
            self.ibe.P_pub = self.P_pub
            self.ibe.initialized = True
            return True
        except Exception as e:
            print(f"Failed to get public params : {e}")
            return False



    def get_private_key(self, email):
        if not self.ibe.initialized:
            if not self.get_public_params_from_server():
                return None
        
        try:
            response = requests.get(f"{self.server_url}/getPrivateKey/{email}")
            response.raise_for_status()
            data = response.json()
            

            self.d_id = self.group.deserialize(bytes.fromhex(data['d_id']))
            self.ID = email
            return self.d_id
        except Exception as e :
            print(f" Failed to get private key: {e}")
            return None
        
    



    

    def encrypt_aes_key(self, recipient_email, aes_key):
        if not self.ibe.initialized:
            if not self.get_public_params_from_server():
                return None, None

        print(f"n\Encrypting for {recipient_email}")
             
        U, ciphertext = self.ibe.encrypt(recipient_email, aes_key)
        print(f"   U: {U}")
        print(f"   Ciphertext: {ciphertext}")
        return U, ciphertext
        # except Exception as e:
        print(f"Encryption failed hereeeee : {e}")
            # return None, None
    


    def decrypt_aes_key(self, U, ciphertext):
        if not self.ibe.initialized:
            if not self.get_public_params_from_server():
                return None

        if not self.d_id:
            prinft(f"No private key available. Get one first !")
            return None

        print("\n Decrypting aes key  ...")
        try:
            message_int = self.ibe.decrypt(
                self.d_id,
                (U, ciphertext)
            )
            aes_key = message_int.to_bytes(32, 'big')
            print(f"Decryption successful")
            return message
        except Exception as e:
            print(f" Decryption failed: {e}")
            return None
    
    def encrypt_and_pack(self, input_path, recipient_email):
        aes_key = AESGCM.generate_key(bit_length=256)
        encrypt_file(input_path, input_path + '.encrypted', aes_key)

        U, ciphertext = self.encrypt_aes_key(recipient_email,aes_key)
        
        # 4. Bundle everything into one file
        output_path = input_path + '.ibe'
        file_out = open(output_path, 'wb')

        U_bytes = bytes.fromhex(U)
        ciphertext_bytes = bytes.fromhex(ciphertext) 

        file_out.write(len(U_bytes).to_bytes(4, "big"))
        file_out.write(U_bytes)
        file_out.write(len(ciphertext_bytes).to_bytes(4, "big"))
        file_out.write(ciphertext_bytes)
        # write the encrypted file data
        file_encrypted = open(input_path + '.encrypted', 'rb')
        file_out.write(file_encrypted.read())

        file_encrypted.close()
        file_out.close()
        return output_path



    def unpack_and_decrypt(self, input_path):
        file_in = open(input_path, 'rb')

        U_size = int.from_bytes(file_in.read(4), "big")
        U_bytes = file_in.read(U_size)
        U = self.group.deserialize(U_bytes)  

        ciphertext_size = int.from_bytes(file_in.read(4), "big")
        ciphertext_bytes = file_in.read(ciphertext_size)
        ciphertext = int.from_bytes(ciphertext_bytes, "big") 
        

        # 3. Decrypt AES key using IBE
        aes_key = self.decrypt_aes_key(U, ciphertext)

        # 4. Decrypt the file chunks
        output_path = input_path.replace('.ibe', '.decrypted')
        file_out = open(output_path, 'wb')
        aesgcm = AESGCM(aes_key)
        decrypt_file(input_file,aes_key)

        return output_path




    