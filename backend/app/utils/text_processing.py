import re


def normalize(text: str) -> str:
    text = text.lower().strip()
    # remove non-alphanumeric except spaces
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> list[str]:
    return normalize(text).split()


def remove_stop_tokens(tokens: list[str], stop_tokens: set[str]) -> list[str]:
    """Remove generic tokens used for periodicity/prefix/suffix normalization."""
    return [t for t in tokens if t not in stop_tokens]


def jaccard_similarity(a_tokens: list[str], b_tokens: list[str]) -> float:
    """Simple token-set similarity for lexical overlap checks."""
    a_set = set(a_tokens)
    b_set = set(b_tokens)
    if not a_set and not b_set:
        return 1.0
    if not a_set or not b_set:
        return 0.0
    return len(a_set & b_set) / len(a_set | b_set)
