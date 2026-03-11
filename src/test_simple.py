from ibe_utils import IBEEncryption

# Créer le système
ibe = IBEEncryption('SS512')
ibe.setup()

# Générer clé pour Alice
cle_alice = ibe.extract("b")

# Chiffrer
message = "b"
U, cipher = ibe.encrypt("b", message)

print('U : ', U)
print('C : ', cipher)


# Déchiffrer
message_recu = ibe.decrypt(cle_alice, (U, cipher), True)
print(f"Message déchiffré: {message_recu}")  # Devrait afficher Hello to me