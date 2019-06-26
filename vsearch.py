def search4vowels(phrase: str) -> set:  # funkcja zwraca zbiór
    """wyswietla samogłoski znalezione w podanym słowie jako argument."""
    vowels = set('aeiou')
    return vowels.intersection(set(phrase))


def search4letters(phrase: str, letters: str = 'aeiou') -> set:
    """zwraca zbiór liter ze zmiennej letters znalezionych w zmiennej phrase"""
    return set(letters).intersection(set(phrase))


search4letters('galaktyka', 'tym')
