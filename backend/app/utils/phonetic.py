import jellyfish


def metaphone(word: str) -> str:
    return jellyfish.metaphone(word)


def soundex(word: str) -> str:
    return jellyfish.soundex(word)


def phonetic_similarity(a: str, b: str) -> bool:
    """Check if two strings are phonetic matches using multiple algorithms."""
    return metaphone(a) == metaphone(b) or soundex(a) == soundex(b)


def spelling_similarity(a: str, b: str) -> float:
    """
    Return normalized spelling similarity in [0, 1].
    Uses Levenshtein distance to catch variants like namaskar/namascar.
    """
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    dist = jellyfish.levenshtein_distance(a.lower(), b.lower())
    denom = max(len(a), len(b))
    return max(0.0, 1.0 - (dist / denom))
