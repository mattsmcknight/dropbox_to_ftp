#!/usr/bin/env python

from ftplib import FTP
from io import BytesIO
import os
import dropbox


def send_to_ftp(filename, server, binary_file):
    with FTP() as ftp:
        server = "192.168.1.97:2221"
        host, port = tuple([item for item in server.split(":")])
        ftp.connect(host, int(port))
        ftp.login()
        ftp.storbinary(f"STOR {filename}", binary_file)

def idempotency(visited_files):
    try:
        os.stat("files.txt")
    except FileNotFoundError:
        with open('files.txt', 'a'):
            pass
    with open("files.txt", 'r') as read_files:
        for line in read_files.readlines():
            visited_files.add(line.strip())
    with open("files.txt", 'w') as files:
        for file_name in visited_files:
            files.write(f"{file_name}\n")
    return visited_files   

def main():
    with open('app_token.txt', 'r') as app_file:
        app_tokens = [ line.strip() for line in app_file.readlines()]
    visited_files = idempotency(set())
    for app_token in app_tokens:
        dbx = dropbox.Dropbox(app_token)
        #print(dbx.users_get_current_account())
        for entry in dbx.files_list_folder('').entries:
            visited_files.add(entry.name)
            meta, response = dbx.files_download(entry.path_lower)
            binary_file = BytesIO(response.content)
            send_to_ftp(entry.name, "192.168.1.97:2221", binary_file)
            visited_files = idempotency(visited_files)

if __name__ == "__main__":
    main()
