from charm.toolbox.pairinggroup import PairingGroup, G1, ZR, pair

class User:
    def __init__(self, P, P_pub):
        self.P = P
        self.P_pub = P_pub
        self.d_id = None
        self.G1 = G1
        self.ZR = ZR



    def save_private_key(d_id):

  
    
    def extract(self, ID):

        
        # Hash de l'identité vers un point de la courbe
        Q_id = self.group.hash(ID,G1)
        d_id = self.s * Q_id
        
        print(f"Private key is generated for id : '{ID}'")
        return d_id
