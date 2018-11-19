from  registration import register_user
from  sshlogin import sshclient,login
import os
import re
import sys

w_file = '/tmp/123.txt'

def add_host_main():
    while True:
        if add_host():
            break
        print("\n\nAgain:")

def add_host():
    print("================Add new host=====================")
    print "register host into file, Authentication method can use password or Certification(eg: /home/cert.pem)"
    print("Input '#q' exit")
    select_auth = str_format("Auth method(p or r):", "^(p|r)")
    password=None
    cert_path=None
    if select_auth == "#q":
        return 1
    host_ip = str_format("Host IP(ip address):", "^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    if host_ip == "#q":
        return 1
    host_port = str_format("Host port(Default 22):", "[0-9]+")
    if host_port == "#q":
        return 1
    if select_auth == 'p':
        password = str_format("Password:", ".*")
        if password == "#q":
            return 1
    elif select_auth == 'r':
        cert_path = str_format("Certpath(absolute path):","^/")
        if cert_path == "#q":
            return 1
    else:
        os.system("clear")
        print ("password and cert path cannot be empty")
        return 0
    name = str_format("User Name:", "^[^ ]+$")
    if name == "#q":
        return 1
    elif not name:
        os.system("clear")
        print("[Warning]:User name cannot be emptyg")
        return 0
    if not password is None or not cert_path is None:
        register_user.registration(host_ip, name, str(host_port), w_file, p=password,cert_path=cert_path)
    return 1

def str_format(lable, rule):
    while True:
        print("{} ('#q' exit)".format(lable))
        temp = raw_input().strip()
        m = re.match(r"{}".format(rule), temp)
        if m:
            break
        elif "port" in lable:
            temp = 22
            break
        elif temp.strip() == "#q":
            os.system("clear")
            break
        os.system("clear")
        print("[Warning]:Invalid format")
    return temp

def ssh_login():
    print("================login into host=====================")
    select_auth = str_format("Auth method(p or r):", "^(p|r)")
    password=None
    cert_path=None
    if select_auth == "#q":
        return 1
    host_ip = str_format("Host IP(ip address):", "^(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    if host_ip == "#q":
        return 1
    elif not host_ip:
        os.system("clear")
        print("[Warning]:remote host ip cannot be empty")
        return 0
    if select_auth == 'p':
        password = str_format("Password:", ".*")
        if password == "#q":
            return 1
    elif select_auth == 'r':
        cert_path = str_format("Certpath(absolute path):","^/")
        if cert_path == "#q":
            return 1
    else:
        os.system("clear")
        print ("password and cert path cannot be empty")
        return 0
    user_init = login.Secret_check(host_ip, w_file)
    find_user = user_init.get_user_info(label=select_auth)
    if find_user:
        tty = sshclient.SSHConnection(find_user['host'], find_user['port'], find_user['user'], password=password, cert=cert_path)
        tty.get_tty(select_auth)

def main():
    while True:
        print("==============AUTOSSH [Menu]=============")
        print(" 1.Connection a host use password\n 2.Connection a host user certification \n 3.Add host\n 4.Enter q to quit\n 5.clean window")
        print("="*40)
        c = raw_input("Please select a:").strip()
        if c == "1":
            ssh_login()
        if c == "2":
            print "2"
        if c == "3":
            add_host_main()
        if c == "clear":
            os.system("clear")
        if c == "q" or c == "Q" or c == "quit":
            print("Bye")
            sys.exit()
        else:
            print("\n")

if __name__ == '__main__':
    #print "register host into file , Authentication method can use password or Certification "
    #print ""
    #register_user.registration('192.168.8.57','root','22',w_file,p='123456')
    #register_user.registration('172.31.19.99','root','22',w_file,cert_path='/tmp/aaa.crt')

    # user = login.Secret_check('192.168.8.57',w_file,pw='123456')
    #
    # if user.check_secret():
    #     ssh_client = sshclient.SSHConnection('192.168.8.57','22','root','123456')
    #     #ssh_client.exec_command("ls")
    #     #ssh_client.close()
    #     ssh_client.load_system_host_keys()
    #     channel = ssh_client.invoke_shell()
    #     interactive.interactive_shell(channel)
    #tty = sshclient.SSHConnection('192.168.8.57','22','root','123456')
    #tty.get_tty()
    main()
