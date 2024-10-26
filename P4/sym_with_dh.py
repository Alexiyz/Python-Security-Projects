import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Diffie-Hellman Key Exchange
def dh_generate_keys(p, g):
    private_key = random.randint(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key

def dh_shared_secret(their_public, my_private, p):
    return pow(their_public, my_private, p)


def derive_key(shared_secret):
    # Derive a 256-bit key using SHA-256
    shared_secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big')
    return hashlib.sha256(shared_secret_bytes).digest()

# Symmetric Encryption (AES)
def encrypt_message(key, plaintext):
    # Encrypt with AES in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = pad(plaintext.encode('utf-8'), AES.block_size)
    return cipher.encrypt(padded_text)

def decrypt_message(key, ciphertext):
    # Decrypt with AES in ECB mode (Not secure)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_text = cipher.decrypt(ciphertext)
    return unpad(padded_text, AES.block_size).decode('utf-8')

# Example usage
# Shared public parameters
p = 57163  # Prime number (in practice, this should be a large number)
g = 5   # Generator

# Alice's keys
alice_private, alice_public = dh_generate_keys(p, g)

# Bob's keys
bob_private, bob_public = dh_generate_keys(p, g)

# Exchange public keys and generate shared secret
alice_shared_secret = dh_shared_secret(bob_public, alice_private, p)
bob_shared_secret = dh_shared_secret(alice_public, bob_private, p)

# Derive symmetric key from shared secret
alice_symmetric_key = derive_key(alice_shared_secret)
bob_symmetric_key = derive_key(bob_shared_secret)

# Encrypt and decrypt a message
message = "Hello, Bob! This is Alice."

# Alice encrypts the message
encrypted_message = encrypt_message(alice_symmetric_key, message)
print("Encrypted message:", encrypted_message)

# Bob decrypts the message
decrypted_message = decrypt_message(bob_symmetric_key, encrypted_message)
print("Decrypted message:", decrypted_message)
