import os
import re
from encryption import user_encryption

class Find_user_infile(object):
    def __init__(self, host , user, w_file, port, password=None , cert_path =None):
        self._host = host
        self._user = user
        self._password = password
        self._cert_path = cert_path
        self._w_file = w_file
        self._port = port

    def judge(self):
        if self._password and self._cert_path:
            print "None password and cert_path"
            return False

    def judge_user_exist(self):
        if os.path.exists(self._w_file):
            with open(self._w_file,'r') as f:
                for line in f.readlines():
                    if re.findall(self._user, line) and re.findall(self._host, line):
                        print "host and user is exist in this file"
                        return False
                return True
        else:
            print "file is not exits,create a new file"
            file = open(self._w_file,'w')
            file.close()
            return True

    def write_user_to_file(self):
        if self.judge_user_exist():
            if self._password:
                storage = user_encryption.Users(self._user, password=self._password)
                with open(self._w_file, 'ab+') as f:
                   f.write(self._host + " " + self._port + " " + storage.username + " " + storage.password + " " + storage.salt + "\n")
            else:
                storage = user_encryption.Users(self._user,cert_path=self._cert_path)
                with open(self._w_file, 'ab+') as f:
                    f.write(self._host + " " + self._port + " " + self._user + " " + storage.cert_path + " " +storage.salt + "\n")