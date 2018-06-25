from Crypto import Random
from Crypto.PublicKey import RSA
import base64
import json
import os


def generate_keys():
	# RSA modulus length must be a multiple of 256 and >= 1024
	modulus_length = 256*4  # use larger value in production
	privatekey = RSA.generate(modulus_length, Random.new().read)
	publickey = privatekey.publickey()
	return privatekey, publickey


def encrypt_message(a_message, publickey):
	encrypted_msg = publickey.encrypt(a_message, 32)[0]
	# base64 encoded strings are database friendly
	encoded_encrypted_msg = base64.b64encode(encrypted_msg)
	return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, privatekey):
	decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
	decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
	return decoded_decrypted_msg

def resetKeys():
	keys = RSA.generate(1024, Random.new().read)

	privHandle = open("privateKeyFile", 'wb')
	privHandle.write(keys.exportKey())
	privHandle.close()

	pubHandle = open("publicKeyFile", 'wb')
	pubHandle.write(keys.publickey().exportKey())
	pubHandle.close()
