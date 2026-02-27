import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    CHROMA_COLLECTION: str = os.getenv("CHROMA_COLLECTION", "titles")
    DISALLOWED_PREFIXES: list[str] = os.getenv("DISALLOWED_PREFIXES", "the,india,samachar,news").split(",")
    DISALLOWED_SUFFIXES: list[str] = os.getenv("DISALLOWED_SUFFIXES", "the,india,samachar,news").split(",")
    DISALLOWED_WORDS: list[str] = os.getenv("DISALLOWED_WORDS", "police,crime,corruption,cbi,cid,army").split(",")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    MIN_VERIFICATION_PROBABILITY_FOR_APPROVAL: float = float(os.getenv("MIN_VERIFICATION_PROBABILITY_FOR_APPROVAL", "0.70"))
    PHONETIC_STRONG_MATCH_SCORE: float = float(os.getenv("PHONETIC_STRONG_MATCH_SCORE", "0.90"))
    SPELLING_SIMILARITY_THRESHOLD: float = float(os.getenv("SPELLING_SIMILARITY_THRESHOLD", "0.84"))
    LEXICAL_THEME_SIMILARITY_THRESHOLD: float = float(os.getenv("LEXICAL_THEME_SIMILARITY_THRESHOLD", "0.75"))


settings = Settings()
