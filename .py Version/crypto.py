#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
Librairie de cryptographie rendue disponible pour le P3 du cours de LINFO1001.

Attention: Cette librairie a été réalisée à des fins purement didactiques et ne peut en aucun cas être considérée comme une solution cryptographique viable pour un programme en dehors du contexte du cours LINFO1001.
"""

def encode(key, plain_text):
	"""
	Chiffre un texte en utilisant une clé de chiffrement.
	Les deux arguments sont fournis sous la forme d'une chaine de caractères.
	L'algorithme utilisé est le chiffrement de Vigenère.
	Attention : cette méthode est "craquée" depuis longtemps, mais elle illustre le fonctionnement d'un algorithme de chiffrement.

	:param (str) key: la clé symétrique
	:param (str) plain_text: le texte à chiffrer
	:return (str): le texte chiffré
	"""
	enc = []
	for i, e in enumerate(plain_text):
		key_c = key[i % len(key)]
		enc_c = chr((ord(e) + ord(key_c)) % 256)
		enc.append(enc_c)
	return "".join(enc)

def decode(key, cipher_text):
	"""
	Déchiffre le texte en utilisant la clé de déchiffrement.
	Les deux arguments sont fournis sous la forme d'une chaine de caractères.
	L'algorithme utilisé est le (dé)chiffrement de Vigenère.
	Attention : cette méthode est "craquée" depuis longtemps, mais elle illustre le fonctionnement d'un algorithme de (dé-)chiffrement.

	:param (str) key: la clé symétrique
	:param (str) cipher_text: le texte crypté
	:return (str): le texte décrypté
	"""
	dec = []
	for i, e in enumerate(cipher_text):
		key_c = key[i % len(key)]
		dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
		dec.append(dec_c)
	return str("".join(dec))

def hashing(to_hash: str) -> str:
    return str(hash(to_hash))

