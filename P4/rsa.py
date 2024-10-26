import random
from math import gcd


def generate_prime_candidate(length):
    p = random.getrandbits(length)
    # Apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p

# Miller-Rabin probabilistic prime test
def is_prime(num, tests=10):
    if num <= 1:
        return False
    elif num <= 3:
        return True
    elif num % 2 == 0 or num % 3 == 0:
        return False

    r = 0
    s = num - 1
    while s % 2 == 0:
        s //= 2
        r += 1

    for _ in range(tests):
        a = random.randint(2, num - 2)
        x = pow(a, s, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False
    return True


def generate_prime_number(length=1024):
    p = 4
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p


def modular_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("No modular inverse exists")
    return x % phi


# RSA Key generation
def generate_keypair(length=1024):
    p = generate_prime_number(length)
    q = generate_prime_number(length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = modular_inverse(e, phi)
    return ((e, n), (d, n))


# Encryption
def encrypt(public_key, plaintext):
    e, n = public_key
    plaintext = int.from_bytes(plaintext.encode('utf-8'), byteorder='big')
    ciphertext = pow(plaintext, e, n)
    return ciphertext


# Decryption
def decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = pow(ciphertext, d, n)
    plaintext = plaintext.to_bytes((plaintext.bit_length() + 7) // 8, byteorder='big')
    return plaintext.decode('utf-8')


# Example usage
public_key, private_key = generate_keypair(512)
message = "Hello world, lets test this RSA implementation!"


encrypted_msg = encrypt(public_key, message)
print("Encrypted message:", encrypted_msg)

decrypted_msg = decrypt(private_key, encrypted_msg)
print("Decrypted message:", decrypted_msg)
