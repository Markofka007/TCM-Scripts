#!/bin/python3

from pwn import *
import sys

if len(sys.argv) != 2:
	print("Invalid Argument")
	print(f"{sys.argv[0]} <sha265sum>")

target_hash = sys.argv[1]
pw_file_path = "/usr/share/wordlists/rockyou.txt"
attempts = 0

with log.progress(f"Attempting to crack {target_hash}\n") as p:
	with open(pw_file_path, "r", encoding="latin-1") as pw_list:
		for pw in pw_list:
			pw = pw.strip("\n").encode("latin-1")
			pw_hash = sha256sumhex(pw)
			p.status(f"[{attempts}] {pw.decode('latin-1')} == {pw_hash}")
			if pw_hash == target_hash:
				p.success(f"{pw.decode('latin-1')} decodes to {pw_hash}")
				exit()
			attempts += 1
		p.failure(f"Password hash not found in the wordlist: {pw_file_path}")