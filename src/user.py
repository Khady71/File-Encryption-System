from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair
from ibe_utils import IBEEncryption
import requests


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
        
    



    

    def encrypt(self, recipient_email, message_original):
        if not self.ibe.initialized:
            if not self.get_public_params_from_server():
                return None, None

        
        print(f"n\Encrypting for {recipient_email}")
             
        U, ciphertext = self.ibe.encrypt(recipient_email, message_original)
        print(f"   U: {U}")
        print(f"   Ciphertext: {ciphertext}")
        return U, ciphertext
        # except Exception as e:
        print(f"Encryption failed hereeeee : {e}")
            # return None, None
    


    def decrypt(self, U, ciphertext):
        if not self.ibe.initialized:
            if not self.get_public_params_from_server():
                return None

        if not self.d_id:
            prinft(f"No private key available. Get one first !")
            return None

        print("\n Decrypting message ...")
        try:
            message = self.ibe.decrypt(
                self.d_id,
                (U, ciphertext),
                decode_to_string=True
            )
            print(f"Decryption successful")
            return message
        except Exception as e:
            print(f" Decryption failed: {e}")
            return None
    