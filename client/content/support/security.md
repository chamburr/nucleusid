---
title: Security
description: Explaining how security works in this project.
---

The encryption and stuff may be complex at first glance. That is why I thought I should explain how
it works in detail.

There are two main algorithms used for encryption, RSA-1024 and AES-128 (CBC). There are also some
other things relevant to this, such as PBKDF2, SHA256 and base64. Let me explain in detail.

## User

Every user is assigned an AES key for the lifetime of the user. This key is kept private forever, it
is never changed and also never stored anywhere on the database.

Furthermore, a user is also assigned a pair of RSA keys. This key is generated based on the master
password, which goes through PBKDF2 and SHA256 to generate a seed. This seed is used for a random
number generator, which helps to generate an RSA private key. The public key is derived and stored
in the database, while the private key is not stored anywhere.

The seed is stored in the JWT token of the login. This is fast because it has already gone through
the very expensive PBKDF2 algorithm. It is also shorter than the actual RSA public key by a lot.

The RSA public key is used to encrypt the AES key, and the encrypted version is stored in the
database, called secret. When a user changes their password, their pair of RSA keys changes since it is derived from the
master password. Hence, the encrypted version of the AES key will be updated via decryption with the
old RSA private key and encryption with the new RSA public key.

## Folder

A folder can also have its own AES key depending on whether the folder is shared. If the folder is
not shared, then the AES key of the owner is used.

When it is shared, a new AES key is generated. This key is stored in the shares table, encrypted by
the user's RSA public key. When a new share is created, the target user's RSA public key is used
to encrypt the AES key, after it is decrypted by the current user's RSA private key.

## Account

This is referring to the account table in the database. The password field in the account is
encrypted by the AES key of the folder that it belongs to. This could either be the folder's unique
AES key or the owner's default key
