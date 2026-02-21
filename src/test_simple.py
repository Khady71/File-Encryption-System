# Exemple d'utilisation basique
from kgc import IBEEncryption

# Créer le système
ibe = IBEEncryption('SS512')

# Configurer
ibe.setup()

# Générer clé pour Alice
cle_alice = ibe.extract("alice")

# Chiffrer
message = 12345
U, cipher = ibe.encrypt("alice", message)

# Déchiffrer
message_recu = ibe.decrypt(cle_alice, (U, cipher))
print(f"Message déchiffré: {message_recu}")  # Devrait afficher 12345