from binascii import unhexlify
import os, hashlib

def salt_and_pepper(byte_password):
    salt = b'XHy5tpl2VHvn83A4_OUOP$x/6VcDBduPZ3wh/QF/b9Fk+fCoXXj12FCdhjc7J+Zry'
    salted = hashlib.pbkdf2_hmac('sha256', byte_password, salt, 700000)

    pepper = bytearray(os.environ.get('AUTH_SECRET').decode('string-escape'))
    return hashlib.pbkdf2_hmac('sha256', salted, pepper, 500000)

def authenticate(password):
    print password
    hashed_password = salt_and_pepper(bytearray(password, 'utf-8'))
    encrypted_password = unhexlify(os.environ.get('AUTH_PASSWORD'))
    return (hashed_password == encrypted_password)
