from app.auth import credentials


def login(username: str, password: str):
    credentials.save(credentials.Credentials(username, password))


def access() -> credentials.Credentials:
    return credentials.read()


def logout():
    credentials.delete()
