"""This portion of my Final project is encrypting my key so I can put it on github without Discord freaking out """

## import cryptographic method, symetric
from cryptography.fernet import Fernet

## Generating key file for decrypting
key = Fernet.generate_key()
with open('mykey.key', 'wb') as mykey:
    mykey.write(key)

## loading key into environment from mykey.key file
with open('mykey.key', 'rb') as mykey:
    key = mykey.read()
    print(key)  # validating key creation

## Encrypt desired file, in this case .env which contains the discord Tokens
f = Fernet(key) # load key value into variable, f
## read original file into memory
with open('.env', 'rb') as original_file:
    original = original_file.read()
    encrypted = f.encrypt(original) # encrypting the original file in memory

## writing now encrypted data back into the directory
with open ('enc_env.csv', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
