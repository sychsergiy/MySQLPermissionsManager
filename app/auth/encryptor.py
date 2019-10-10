from simplecrypt import encrypt, decrypt


class Encryptor(object):
    def __init__(self, key: str):
        self._key = key

    def encrypt(self, string: str) -> bytes:
        return encrypt(self._key, string)

    def decrypt(self, encrypted: bytes) -> str:
        return decrypt(self._key, encrypted).decode()


def load_key() -> str:
    return "DAr1DgtgM1"
