
import math

def racine_carre(x):
    """
    >>> racine_carre(4)
    2
    >>> racine_carre(25)
    5
    """
    res = x ** 0.5
    if res.is_integer():
        return int(res)
    return res
