from binascii import unhexlify
import os, hashlib

class AuthenticationException(Exception):
    pass

def get_auth_cert():
    cert_file = open('/run/secrets/auth_cert', 'r')
    cert_content = cert_file.readlines()

    encrypted_password = cert_content[0].strip()
    pepper = reduce(lambda x, y: x + y, cert_content[1:]).encode('string_escape')

    return encrypted_password, pepper

def salt_and_pepper(byte_password, pepper):
    salt = b'XHy5tpl2VHvn83A4_OUOP$x/6VcDBduPZ3wh/QF/b9Fk+fCoXXj12FCdhjc7J+Zry'
    salted = hashlib.pbkdf2_hmac('sha256', byte_password, salt, 700000)
    return hashlib.pbkdf2_hmac('sha256', salted, pepper, 500000)

def authenticate(password):
    encrypted_password, pepper = get_auth_cert()
    encrypted_password = unhexlify(encrypted_password)
    hashed_password = salt_and_pepper(bytearray(password, 'utf-8'),
        bytearray(pepper.decode('string-escape')))

    auth_check = (hashed_password == encrypted_password)
    print ("Authenticating event....%s" % ("Success" if auth_check else "Failure"))

    if not auth_check:
        raise AuthenticationException()
