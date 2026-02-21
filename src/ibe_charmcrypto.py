from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.ibenc.ibenc_bf01 import IBE_BonehFranklin

group = PairingGroup('MNT224', secparam=1024)
ibe = IBE_BonehFranklin(group)

# Setup
(master_public_key, master_secret_key) = ibe.setup()

# Extract private key for identity
ID = 'user@email.com'
private_key = ibe.extract(master_secret_key, ID)

# Encrypt to identity
msg = b"hello world!!!!!"
cipher_text = ibe.encrypt(master_public_key, ID, msg)

# Decrypt
decrypted = ibe.decrypt(master_public_key, private_key, cipher_text)
assert decrypted == msg