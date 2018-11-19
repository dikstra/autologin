import random
import hashlib

class Users(object):
    def __init__(self, username, password=None ,cert_path=None):
        self.username = username
        self.salt = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        if password:
            self.password = get_md5(password + self.salt)
        else:
            self.cert_path = get_md5(cert_path + self.salt)


def get_md5(s):
    #return hashlib.md5(s.encode('utf-8')).hexdigest()
    return s.encode('utf-8').hexdigest()
