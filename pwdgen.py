import random
import string

#length = password length
def generate_password(length: int = 12):
    vocabulary = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(random.choice(vocabulary) for i in range(length))
    return pwd

password = generate_password()
print(f'Generated password: {password}')