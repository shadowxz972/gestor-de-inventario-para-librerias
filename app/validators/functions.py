def validate_positive_int_numbers(*values:int) -> bool:
    for value in values:
        if value < 0:
            return False
    return True