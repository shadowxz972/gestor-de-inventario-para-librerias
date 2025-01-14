from app.validators.constants import MAX_LENGTH_TITLE


def title_validation(title: str) -> str:
    """
    Valida el formato del titulo
    :param title:
    :return: title
    """
    if len(title) > MAX_LENGTH_TITLE:
        raise ValueError(f"El titulo no puede tener mas de {MAX_LENGTH_TITLE} caracteres")
    if len(title) == 0:
        raise ValueError(f"El titulo no puede estar vacio")
    return title


def author_validation(author: str) -> str:
    """
    Valida el formato del autor
    :param author:
    :return: author
    """
    if len(author) == 0:
        raise ValueError(f"El nombre del autor no puede ser vacio")
    return author


def category_validation(category: str) -> str:
    """
    Valida el formato de la categoria
    :param category:
    :return: category
    """
    if len(category) == 0:
        raise ValueError(f"El nombre del categoria no puede ser vacio")
    return category


def price_validation(price: float) -> float:
    """
    Valida el formato del precio
    :param price:
    :return: price
    """
    if price == 0:
        raise ValueError(f"El precio no puede ser vacio")
    if price < 0:
        raise ValueError(f"El precio no puede ser negativo")
    return price


def stock_validation(stock: int) -> int:
    """
    Valida el formato del stock
    :param stock:
    :return:
    """
    if stock < 0:
        raise ValueError(f"El stock no puede ser vacio")
    return stock
