from __future__ import annotations

import base64
import math
import random

from typing import Union

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class SecretCipher:
    def __init__(self, seed: bytes, key: RSA):
        self._seed = seed
        self._key = key

        self._cipher = PKCS1_OAEP.new(key)

    @classmethod
    def create(cls, password: str, identifier: int) -> SecretCipher:
        seed = PBKDF2(
            password,
            str(identifier).encode(),
            count=100000,
            hmac_hash_module=SHA512,
        )

        return cls.from_seed(seed)

    @classmethod
    def from_seed(cls, seed: Union[str, bytes]) -> SecretCipher:
        if isinstance(seed, str):
            seed = base64.b64decode(seed)

        rng = random.Random(seed)
        key = RSA.generate(1024, rng.randbytes)

        return cls(seed, key)

    @classmethod
    def from_public_key(cls, key: str) -> SecretCipher:
        return cls(b"", RSA.import_key(key))

    @property
    def seed(self) -> str:
        return base64.b64encode(self._seed).decode()

    @property
    def private_key(self):
        return self._key.export_key().decode()

    @property
    def public_key(self) -> str:
        return self._key.public_key().export_key().decode()

    def encrypt(self, secret: bytes) -> str:
        return base64.b64encode(self._cipher.encrypt(secret)).decode()

    def decrypt(self, secret: str) -> bytes:
        return self._cipher.decrypt(base64.b64decode(secret))

    def re_encrypt(self, old: SecretCipher, secret: str) -> str:
        return self.encrypt(old.decrypt(secret))


class DataCipher:
    def __init__(self, key: bytes):
        self._key = key

    @classmethod
    def create(cls) -> DataCipher:
        key = get_random_bytes(16)

        return cls.from_key(key)

    @classmethod
    def from_key(cls, key: bytes) -> DataCipher:
        return DataCipher(key)

    @property
    def key(self) -> bytes:
        return self._key

    def encrypt(self, data: str) -> str:
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self._key, AES.MODE_CBC, iv)

        cipher_text = cipher.encrypt(pad(data.encode(), AES.block_size))

        return (
            base64.b64encode(iv).decode()
            + base64.b64encode(cipher_text).decode()
        )

    def decrypt(self, data: str) -> str:
        if not data:
            return data

        length = math.floor((AES.block_size + 2) / 3) * 4

        iv = base64.b64decode(data[:length])
        cipher_text = base64.b64decode(data[length:])

        cipher = AES.new(self._key, AES.MODE_CBC, iv)

        return unpad(cipher.decrypt(cipher_text), AES.block_size).decode()

    def re_encrypt(self, old: DataCipher, data: str) -> str:
        return self.encrypt(old.decrypt(data))

    def encrypt_account(self, account: dict) -> dict:
        account["password"] = self.encrypt(account["password"])

        return account

    def decrypt_account(self, account: dict) -> dict:
        account["password"] = self.decrypt(account["password"])

        return account
