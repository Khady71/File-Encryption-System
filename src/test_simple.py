from ibe_utils import IBEEncryption

# Créer le système
ibe = IBEEncryption('SS512')
ibe.setup()

# Générer clé pour Alice
cle_alice = ibe.extract("alice@a.com")

# Chiffrer
message = "Hello To Me"
U, cipher = ibe.encrypt("alice@a.com", message)

print('U : ', U)
print('C : ', cipher)

U = ibe.group.deserialize(bytes.fromhex(U))   
message_recu = ibe.decrypt(cle_alice, (U, cipher), True)
print(f"Message déchiffré: {message_recu}")  # Devrait afficher Hello To Me