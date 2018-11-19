from registration import modify_user


def registration(host, u, port, w_file, p=None,cert_path=None):
    write_to_file =modify_user.Find_user_infile(host,u,w_file,port,p,cert_path)
    write_to_file.write_user_to_file()