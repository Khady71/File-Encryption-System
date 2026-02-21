from kgc import IBEEncryption

def test_ibe_encryption():
    print("=" * 50)
    print("TEST DU SYSTÈME IBE")
    print("=" * 50)
    
    # 1. Initialisation
    print("\n1️⃣ Création du système IBE")
    ibe = IBEEncryption('SS512')
    
    # 2. Setup
    print("\n2️⃣ Configuration du système")
    P, P_pub, s = ibe.setup()
    print(f"   Générateur P: {P}")
    print(f"   Clé publique maître: {P_pub}")
    
    # 3. Extraction de clé pour Alice
    print("\n3️⃣ Génération de la clé privée pour Alice")
    d_alice = ibe.extract("alice@email.com")
    
    # 4. Chiffrement pour Alice
    print("\n4️⃣ Chiffrement d'un message pour Alice")
    message_original = "Hello IBE World!"
    print(f"   Message original: '{message_original}'")
    
    U, ciphertext = ibe.encrypt("alice@email.com", message_original)
    print(f"   U: {U}")
    print(f"   Ciphertext: {ciphertext}")
    
    # 5. Déchiffrement par Alice
    print("\n5️⃣ Déchiffrement par Alice")
    message_dechiffre = ibe.decrypt(d_alice, (U, ciphertext), decode_to_string=True)
    print(f"   Message déchiffré: '{message_dechiffre}'")
    
    print("\n" + "=" * 50)
    print("TESTS TERMINÉS")
    print("=" * 50)

# Exécution des tests
if __name__ == "__main__":
    
    test_ibe_encryption()