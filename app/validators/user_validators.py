def username_validation(username: str) -> str:
    if len(username) == 0:
        raise ValueError('El usuario no puede estar vacio')
    return username


def hashed_password_validation(password: str) -> str:
    if len(password) == 0:
        raise ValueError('La contraseña no puede estar vacia')
    return password
