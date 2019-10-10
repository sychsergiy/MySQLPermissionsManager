import typing as t

from app.auth.encryptor import Encryptor, load_key

CREDENTIALS_FILE_PATH = ".creds"

encryptor = Encryptor(load_key())


class Credentials(t.NamedTuple):
    username: str
    password: str


def read() -> Credentials:
    with open(CREDENTIALS_FILE_PATH, "rb") as file:
        content = file.read()
        decrypted = encryptor.decrypt(content)
        username, password = decrypted.split(":")
        return Credentials(username, password)


def save(credentials: Credentials):
    with open(CREDENTIALS_FILE_PATH, "wb") as file:
        creds = f"{credentials.username}:{credentials.password}"
        file.write(encryptor.encrypt(creds))


def delete():
    with open(CREDENTIALS_FILE_PATH, "wb") as file:
        file.write(b"")
