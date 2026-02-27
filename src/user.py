from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair
from ibe_utils import IBEEncryption, element_to_storable, storable_to_element
import requests

class User:
    def __init__(self, P=None, P_pub=None):
        
        self.P = P
        self.P_pub = P_pub
        self.d_id = None
        self.ID = None
        self.server_url = "http://localhost:8000"

        if P is not None and P_pub is not None:
            self.ibe = IBEEncryption('SS512')
            self.ibe.P = P
            self.ibe.P_pub = P_pub
            self.ibe.initialized = True
        else:
            self.ibe = None
    



    def get_public_params_from_server(self):
        try:
            response = requests.get(f"{self.server_url}/setup")
            response.raise_for_status()
            data = response.json()

            self.P = storable_to_element(data['P'])
            self.P_pub = storable_to_element(data['P_pub'])

            if not self.ibe:
                self.ibe = IBEEncryption('SS512')
            self.ibe.P = self.P
            self.ibe.P_pub = self.P_pub
            return True
        except Exception as e:
            print(f"Failed to get public params : {e}")
            return False



    def get_private_key(self, email):
        if not self.ibe:
            if not self.get_public_params_from_server():
                return None
        
        try:
            response = requests.get(f"{self.server_url}/getPrivateKey/{email}")
            response.raise_for_status()
            data = response.json()

            self.d_id = storable_to_element(data['d_id'])
            self.ID = email
            return self.d_id
        except Exception as e :
            print(f" Failed to get private key: {e}")
            return None
        
    



    

    def encrypt(self, recipient_email, message_original):
        if not self.ibe:
            if not self.get_public_params_from_server():
                return None, None

        print(f"n\Encrypting for {recipient_email}")
       
        # try:      
        U, ciphertext = self.ibe.encrypt(recipient_email, self.P, message_original)
        print(f"   U: {U}")
        print(f"   Ciphertext: {ciphertext}")
        return U, ciphertext
        # except Exception as e:
        print(f"Encryption failed hereeeee : {e}")
            # return None, None
    


    def decrypt(self, U, ciphertext):
        if not self.ibe:
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
    

