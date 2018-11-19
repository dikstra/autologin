import re
from encryption import user_encryption

class Secret_check(object):
    def __init__(self,hostip, w_file,pw=None,port=None,cert_path=None):
        self._hostip = hostip
        self._w_file =w_file
        if port:
            self._port = port
        else:
            self._port = "22"
        self._password =pw
        self._cert_path =cert_path

    def check_secret(self):
        rst = self.get_user_info()
        if rst:
            if rst.has_key('password'):
                if rst['password'] == user_encryption.get_md5(self._password+ rst['salt']):
                    return 'succeeded'
                else:
                    return 'wrong password'
            if rst.has_key('cert_path'):
                if rst['cert_path'] == user_encryption.get_md5(self._cert_path + rst['salt']):
                    return 'succeeded'
                else:
                    return 'wrong cert file'


    def get_user_info(self,label=None):
        with open(self._w_file, 'r') as f:
            user_list = "".join([line for line in f.readlines() if re.findall(self._hostip, line)]).split()
            if user_list:
                if self._password or label =='p':
                    user_info = {
                        "host": user_list[0],
                        "port": user_list[1],
                        "user": user_list[2],
                        "password": user_list[3],
                        "salt": user_list[4]
                    }
                    # return "".join([line for line in f.readlines() if re.match(host_ip,line)]).split()
                    # print user_info
                    return user_info
                elif self._cert_path or label == 'r':
                    user_info = {
                        "host": user_list[0],
                        "port": user_list[1],
                        "user": user_list[2],
                        "cert_path": user_list[3],
                        "salt": user_list[4]
                    }
                    return user_info
            else:
                print "wrong record in file"
                return False
