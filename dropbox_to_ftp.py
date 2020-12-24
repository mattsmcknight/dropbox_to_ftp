#!/usr/bin/env python

from ftplib import FTP
import fire

def send_to_ftp(filename, server, binary_file):
    with FTP() as ftp:
        server = "192.168.1.97:2221"
        host, port = tuple([item for item in server.split(":")])
        ftp.connect(host, int(port))
        ftp.login()
        ftp.storbinary(f"STOR {filename}", binary_file)

def main():
    
    with open(filename, 'rb') as binary_file:
        send_to_ftp(filename, server, binary_file)

if __name__ == "__main__":
    #fire.Fire(main)
