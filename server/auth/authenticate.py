from __future__ import print_function
from binascii import unhexlify
import os, ast, hashlib

class AuthenticationException(Exception):
    pass

def get_auth_cert():
    with open('/run/secrets/api_auth_certificate', 'r') as cert:
        auth_params_dict = ast.literal_eval(cert.read().replace('\n ', ''))
        return auth_params_dict['encrypted_password'], auth_params_dict['pepper']

def salt_and_pepper(byte_password, pepper):
    salt = b'XHy5tpl2VHvn83A4_OUOP$x/6VcDBduPZ3wh/QF/b9Fk+fCoXXj12FCdhjc7J+Zry'
    salted = hashlib.pbkdf2_hmac('sha256', byte_password, salt, 700000)
    return hashlib.pbkdf2_hmac('sha256', salted, pepper, 500000)

def authenticate(password):
    print ("Authenticating event....", end='')

    try:
        encrypted_password, pepper = get_auth_cert()
        encrypted_password = unhexlify(encrypted_password)
        hashed_password = salt_and_pepper(bytearray(password, 'utf-8'),
            bytearray(pepper.decode('string-escape')))

        auth_check = (hashed_password == encrypted_password)
        print ("Success" if auth_check else "Failure")

        if not auth_check:
            raise AuthenticationException()
    except AuthenticationException:
        raise
    except Exception:
        print ("ERROR")
        raise
