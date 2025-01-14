from datetime import date


def quantity_validation(quantity: int) -> int:
    if quantity < 0:
        raise ValueError("la cantidad no debe ser negativa")
    return quantity


def total_price_validation(total_price: float) -> float:
    if total_price < 0:
        raise ValueError("El precio total no debe ser negativa")
    return total_price


def date_validation(date_obj: date) -> date:
    if date_obj < date.today():
        raise ValueError("La fecha no puede ser futura")
    return date_obj
