from ibe_utils import IBEEncryption

# Créer le système
ibe = IBEEncryption('SS512')
ibe.setup()

# Générer clé pour Alice
cle_alice = ibe.extract("alice")

# Chiffrer
message = "Hello to me"
U, cipher = ibe.encrypt("alice", message)


# Déchiffrer
message_recu = ibe.decrypt(cle_alice, (U, cipher))
print(f"Message déchiffré: {message_recu}")  # Devrait afficher Hello to me