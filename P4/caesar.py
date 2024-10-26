import string

def enc_caesar(cipher, key):
    shift = key % 26

    trans_table = str.maketrans(string.ascii_letters, string.ascii_letters[shift:] + string.ascii_letters[:shift])

    return cipher.translate(trans_table)

def dec_caesar(cipher, key):
    shift = 26 - (key % 26)
    trans_table = str.maketrans(string.ascii_letters, string.ascii_letters[shift:] + string.ascii_letters[:shift])
    return cipher.translate(trans_table).swapcase()

message = 'Python is great, Python is awesome!'
key = 3

print(f'1: {message}')
print(f'2: {enc_caesar(message, key)}')
print(f'3: {dec_caesar(enc_caesar(message,key), key)}')

