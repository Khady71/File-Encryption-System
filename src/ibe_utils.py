from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, GT, pair
from charm.toolbox.hash_module import Hash

from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair, serialize, deserialize
from charm.toolbox.hash_module import Hash
import base64




class IBEEncryption:
    def __init__(self, group_curve='SS512'):
        self.group = PairingGroup(group_curve)
       
        self.P = None          # Générateur public
        self.P_pub = None      # Clé publique maître
        self.s = None          # Secret maître (privé)
        self.initialized = False
        
        print(f" Système IBE initialisé avec la courbe {group_curve}")
    
    # =========================
    # Setup
    # =========================
    
    def setup(self):
        self.P = self.group.random(G1)
        self.s = self.group.random(ZR)
        self.P_pub = self.s * self.P
        self.initialized = True
        print("Publics parameters are successfully generated")
        return self.P, self.P_pub, self.s
    

    # =========================
    # Extract
    # =========================
    def extract(self, ID):
        
        Q_id = self.group.hash(ID,G1)
        d_id = self.s * Q_id
        
        print(f"Private key is generated for ID : '{ID}'")
        return d_id

    
    # =========================
    # Encrypt
    # =========================
    
    def encrypt(self, ID, message, return_as_int=True):
    
        # if not self.initialized:
        #     raise Exception("The system is not initialized. Run setup() before")
        
        # Convertir le message en entier si nécessaire


        if isinstance(message, str):
            message_int = int.from_bytes(message.encode(), 'big')
        else:
            message_int = message
        
        
        Q_id = self.group.hash(ID,G1)
        r = self.group.random(ZR)
        
        U = r * self.P
        
        g_id = pair(Q_id, self.P_pub) ** r
        g_id_bytes = self.group.serialize(g_id)

        key = self.group.hash(g_id_bytes, ZR)
        
        ciphertext = message_int ^ int(key)
        
        print(f"Message chiffré pour '{ID}'")
        U_bytes = self.group.serialize(U)
        U_hex = U_bytes.hex()
        return (U_hex, ciphertext)
    
    # =========================
    # Decrypt
    # =========================
    
    def decrypt(self, d_id, ciphertext, decode_to_string=False):
        
     
        U, V = ciphertext
        # # print('U : ', U)
        # # print('V : ', V)
        # print("type U:", type(U))
        # print("type d_id:", type(d_id))        
        g_id = pair(d_id, U)
       
        g_id_bytes = self.group.serialize(g_id)
        
        key = self.group.hash(g_id_bytes, ZR)
        
        message_int = V ^ int(key)
        
        # Convertir en string 
        if decode_to_string:
            try:
                message = message_int.to_bytes(
                    (message_int.bit_length() + 7) // 8, 'big'
                ).decode()
            except:
                message = str(message_int)
        else:
            message = message_int
        
        print("Message is decrypted successfully")
        return message
    
    # =========================
    # Méthodes utilitaires
    # =========================
    
    def get_public_params(self):
        if not self.initialized:
            return None
        return {
            'P': self.P,
            'P_pub': self.P_pub,
            'group': self.group
        }
    
    def __str__(self):
        """Représentation string de l'objet"""
        status = "initialisé" if self.initialized else "non initialisé"
        return f"IBEEncryption(système={status})"

    

