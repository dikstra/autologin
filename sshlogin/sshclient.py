#coding=utf-8
import paramiko
import os
import getpass
from sshlogin import interactive
from  sshlogin import login

class SSHConnection(object):
    w_file = '/tmp/123.txt'
    def __init__(self, hostip, port, username, password=None, cert=None):
        self._host = hostip
        self._port = int(port)
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._cert = cert
        #self._connect()

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        if self._cert:
            transport.connect(username=self._username, pkey=self._cert)
        else:
            transport.connect(username=self._username, password=self._password)
        self._transport = transport

    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)

    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)

    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            print data.strip()
            return data
        err = stderr.read()
        if len(err) > 0:
            print err.strip()
            return err

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()

    def get_tty(self,auth):
        tran = paramiko.Transport((self._host, self._port))
        #if self._cert:
        #    tran.connect(username=self._username, pkey=self._cert)
        #else:
        #    tran.connect(username=self._username, password=self._password)
        #self._transport = tran
        #tran = self._transport
        tran.start_client()
        default_auth = "p"
        #auth = input('Auth by (p)assword or (r)sa key[%s] ' % default_auth)
        #auth = "r"
        if len(auth) == 0:
            auth = default_auth

        if auth == 'r':
            #default_path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
            #path = input('RSA key [%s]: ' % default_path)
            #if len(path) == 0:
            #    path = default_path
            user = login.Secret_check(self._host, self.w_file, cert_path=self._cert)
            if user.check_secret():
                try:
                    key = paramiko.RSAKey.from_private_key_file(self._cert)
                except paramiko.PasswordRequiredException:
                    #password = getpass.getpass('RSA key password: ')
                    #key = paramiko.RSAKey.from_private_key_file(path, password)
                    print "error in key file"
                tran.auth_publickey(self._username, key)
        else:
            user = login.Secret_check(self._host, self.w_file, pw=self._password)
            if user.check_secret():
                #pw = getpass.getpass('Password for %s@%s: ' % (self._username, self._host))
                tran.auth_password(self._username, self._password)
            else:
                print "password checking failed"
        chan = tran.open_session()
        chan.get_pty()
        chan.invoke_shell()
        interactive.interactive_shell(chan)
