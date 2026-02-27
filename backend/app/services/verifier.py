from ..config import settings
from ..db.chroma_client import get_collection
from ..db.manager import get_db_manager
from ..utils import phonetic, text_processing
from typing import List, Dict, Any, Set
from ..schemas import RuleViolation
import re
import json
from pathlib import Path


class TitleVerifier:
    PERIODICITY_TOKENS = {
        "daily", "weekly", "monthly", "fortnightly", "biweekly",
        "morning", "evening", "nightly", "sunday", "monday",
        "tuesday", "wednesday", "thursday", "friday", "saturday",
    }

    DEFAULT_THEME_LEXICON = {
        "morning": {"morning", "sunrise", "dawn", "prabhat"},
        "evening": {"evening", "sandhya", "sunset", "night"},
        "daily": {"daily", "pratidin", "everyday"},
        "news": {"news", "samachar", "bulletin", "dispatch", "chronicle", "herald", "gazette"},
        "business": {"business", "finance", "financial", "trade", "commerce"},
        "sports": {"sports", "sport", "khel"},
        "politics": {"politics", "political", "rajneeti"},
    }

    def __init__(self):
        self.collection = get_collection()
        self.db_manager = get_db_manager()
        self.THEME_LEXICON = self._load_theme_lexicon()
        self._edge_stop_tokens = set(settings.DISALLOWED_PREFIXES + settings.DISALLOWED_SUFFIXES) | self.PERIODICITY_TOKENS
        self._cache_ready = False
        self._refresh_title_cache()

    def _load_theme_lexicon(self) -> Dict[str, Set[str]]:
        """Load semantic lexicon from resource file, fallback to defaults."""
        resource_path = Path(__file__).resolve().parent.parent / "resources" / "semantic_lexicon.json"
        if resource_path.exists():
            try:
                with resource_path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
                return {k: set(v) for k, v in raw.items() if isinstance(v, list)}
            except Exception:
                pass
        return self.DEFAULT_THEME_LEXICON

    def _refresh_title_cache(self):
        """Load indexed views of existing titles for fast rule checks."""
        self._titles: List[str] = self.db_manager.get_all_titles()
        self._normalized_to_title: Dict[str, str] = {}
        self._normalized_set: set[str] = set()
        self._core_index: Dict[str, List[str]] = {}
        self._core_set: set[str] = set()
        self._core_to_title: Dict[str, str] = {}
        self._theme_signature_index: Dict[str, List[str]] = {}
        self._simplified_tokens_by_title: Dict[str, Set[str]] = {}
        self._token_inverted_index: Dict[str, Set[str]] = {}

        for t in self._titles:
            self._index_single_title(t)
        self._cache_ready = True

    def _index_single_title(self, t: str) -> None:
        """Incrementally index a single title into in-memory structures."""
        norm = text_processing.normalize(t)
        if not norm:
            return

        self._normalized_set.add(norm)
        self._normalized_to_title.setdefault(norm, t)

        tokens = norm.split()
        core = " ".join(text_processing.remove_stop_tokens(tokens, self._edge_stop_tokens))
        if core:
            self._core_index.setdefault(core, []).append(t)
            self._core_set.add(core)
            self._core_to_title.setdefault(core, t)

        sig = self._canonical_signature(tokens)
        if sig:
            self._theme_signature_index.setdefault(sig, []).append(t)

        simplified = set(text_processing.remove_stop_tokens(tokens, self._edge_stop_tokens))
        self._simplified_tokens_by_title[t] = simplified
        for tok in simplified:
            self._token_inverted_index.setdefault(tok, set()).add(t)

    def invalidate_cache(self) -> None:
        """Invalidate/rebuild index cache after bulk DB mutations."""
        self._refresh_title_cache()

    def _canonical_signature(self, tokens: List[str]) -> str:
        """Map tokens to canonical concepts and build a stable signature."""
        canonical = []
        for tok in tokens:
            mapped = tok
            for concept, variants in self.THEME_LEXICON.items():
                if tok in variants:
                    mapped = concept
                    break
            canonical.append(mapped)
        # Remove generic determiners for signature stability.
        canonical = [c for c in canonical if c not in {"the", "a", "an"}]
        return " ".join(canonical)

    def _check_disallowed_words(self, title: str) -> List[RuleViolation]:
        violations = []
        tokens = text_processing.tokenize(title)
        for word in settings.DISALLOWED_WORDS:
            if word in tokens:
                violations.append(RuleViolation(rule="disallowed_word", message=f"Title contains disallowed word '{word}'"))
        return violations

    def _check_prefix_suffix(self, title: str) -> List[RuleViolation]:
        violations = []
        norm = text_processing.normalize(title)
        tokens = norm.split()
        core = " ".join(text_processing.remove_stop_tokens(tokens, self._edge_stop_tokens))
        resembles_existing = bool(core and core in self._core_index)

        for prefix in settings.DISALLOWED_PREFIXES:
            if norm.startswith(prefix + " "):
                if resembles_existing:
                    violations.append(RuleViolation(
                        rule="disallowed_prefix",
                        message=f"Title starts with disallowed prefix '{prefix}' and resembles existing title '{self._core_index[core][0]}'",
                    ))
        for suffix in settings.DISALLOWED_SUFFIXES:
            if norm.endswith(" " + suffix):
                if resembles_existing:
                    violations.append(RuleViolation(
                        rule="disallowed_suffix",
                        message=f"Title ends with disallowed suffix '{suffix}' and resembles existing title '{self._core_index[core][0]}'",
                    ))
        return violations

    def _check_combination(self, title: str) -> List[RuleViolation]:
        violations = []
        norm = text_processing.normalize(title)
        tokens = norm.split()

        # Check if title can be split into two existing titles.
        for i in range(1, len(tokens)):
            left = " ".join(tokens[:i])
            right = " ".join(tokens[i:])

            # Raw normalized split check.
            if left in self._normalized_set and right in self._normalized_set and left != right:
                violations.append(
                    RuleViolation(
                        rule="combination",
                        message=(
                            f"Title appears to combine existing titles "
                            f"'{self._normalized_to_title[left]}' and '{self._normalized_to_title[right]}'"
                        ),
                    )
                )
                break

            # Core-token split check (handles leading/trailing generic words).
            left_core = " ".join(text_processing.remove_stop_tokens(left.split(), self._edge_stop_tokens))
            right_core = " ".join(text_processing.remove_stop_tokens(right.split(), self._edge_stop_tokens))
            if left_core in self._core_set and right_core in self._core_set and left_core != right_core:
                violations.append(
                    RuleViolation(
                        rule="combination",
                        message=(
                            f"Title appears to combine existing titles "
                            f"'{self._core_to_title[left_core]}' and '{self._core_to_title[right_core]}'"
                        ),
                    )
                )
                break
        return violations

    def _check_semantic_similarity(self, title: str):
        # query vector and fetch top matches
        try:
            query_res = self.collection.query(
                query_texts=[title],
                n_results=8,
            )
            if query_res and query_res.get("distances"):
                return query_res
        except Exception:
            return None
        return None

    def _check_periodicity(self, title: str) -> List[RuleViolation]:
        """Disallow adding periodicity tokens to existing titles."""
        violations = []
        norm = text_processing.normalize(title)
        tokens = norm.split()
        for tok in self.PERIODICITY_TOKENS:
            if tok in tokens:
                candidate = re.sub(r"\b" + re.escape(tok) + r"\b", "", norm).strip()
                candidate = re.sub(r"\s+", " ", candidate)
                if candidate in self._normalized_set:
                    violations.append(
                        RuleViolation(
                            rule="periodicity",
                            message=(
                                f"Title adds periodicity token '{tok}' to existing title "
                                f"'{self._normalized_to_title[candidate]}'"
                            ),
                        )
                    )
                    break
        return violations

    def _check_cross_language(self, title: str) -> List[RuleViolation]:
        """Cross-language and conceptual theme matching via canonical signatures."""
        violations = []
        norm = text_processing.normalize(title)
        tokens = norm.split()
        sig = self._canonical_signature(tokens)
        if sig and sig in self._theme_signature_index:
            existing = self._theme_signature_index[sig][0]
            if text_processing.normalize(existing) != norm:
                violations.append(
                    RuleViolation(
                        rule="cross_language",
                        message=f"Title has same conceptual/cross-language meaning as existing title '{existing}'",
                    )
                )

        # Lexical-concept overlap check for same-theme variants.
        simplified = set(text_processing.remove_stop_tokens(tokens, self._edge_stop_tokens))
        candidate_titles: Set[str] = set()
        for tok in simplified:
            candidate_titles |= self._token_inverted_index.get(tok, set())

        for existing in candidate_titles:
            e_simplified = list(self._simplified_tokens_by_title.get(existing, set()))
            sim = text_processing.jaccard_similarity(list(simplified), e_simplified)
            if sim >= settings.LEXICAL_THEME_SIMILARITY_THRESHOLD and norm != text_processing.normalize(existing):
                violations.append(
                    RuleViolation(
                        rule="conceptual_theme",
                        message=f"Title conveys same conceptual theme as existing title '{existing}'",
                    )
                )
                break
        return violations

    def verify(self, title: str):
        violations: List[RuleViolation] = []
        if not self._cache_ready:
            self._refresh_title_cache()

        violations.extend(self._check_disallowed_words(title))
        violations.extend(self._check_prefix_suffix(title))
        violations.extend(self._check_combination(title))

        sim_data = self._check_semantic_similarity(title)
        similarity_score = 0.0
        similar_titles = []
        if sim_data and len(sim_data['distances'][0]) > 0:
            # chroma returns distances, convert to similarity
            # for sentence-transformers, distances are 1 - cosine
            distances = sim_data['distances'][0]
            similarities = [1 - d for d in distances]
            similarity_score = float(max(similarities))
            
            # Get top similar titles
            top_texts = sim_data['documents'][0]
            similar_titles = [t for t in top_texts if t and t.lower() != title.lower()][:3]
            
            # phonetic match
            if top_texts:
                top_text = top_texts[0]
                if phonetic.phonetic_similarity(title, top_text):
                    similarity_score = max(similarity_score, settings.PHONETIC_STRONG_MATCH_SCORE)
                    violations.append(
                        RuleViolation(
                            rule="phonetic_similarity",
                            message=f"Title sounds very similar to existing title '{top_text}'",
                        )
                    )

                # Spelling-variation protection (e.g., Namaskar/Namascar)
                norm_title = text_processing.normalize(title)
                norm_top = text_processing.normalize(top_text)
                spell_sim = phonetic.spelling_similarity(norm_title, norm_top)
                if spell_sim >= settings.SPELLING_SIMILARITY_THRESHOLD and norm_title != norm_top:
                    similarity_score = max(similarity_score, spell_sim)
                    violations.append(
                        RuleViolation(
                            rule="spelling_variation",
                            message=f"Title appears to be a spelling variation of existing title '{top_text}'",
                        )
                    )

        violations.extend(self._check_periodicity(title))
        violations.extend(self._check_cross_language(title))

        probability = max(0.0, 1.0 - similarity_score)

        # Rule-driven penalties: hard compliance failures should not show high approval chance.
        hard_rules = {"disallowed_word", "combination", "cross_language", "periodicity", "conceptual_theme"}
        violation_rules = {v.rule for v in violations}
        if violation_rules:
            probability = min(probability, 0.30)
        if violation_rules & hard_rules:
            probability = min(probability, 0.10)

        # Keep compatibility with acceptance expectation: probability <= (1 - similarity).
        probability = min(probability, max(0.0, 1.0 - similarity_score))

        # Deduplicate repeated violations.
        dedup: Dict[tuple[str, str], RuleViolation] = {}
        for v in violations:
            dedup[(v.rule, v.message)] = v
        violations = list(dedup.values())
        
        # persist title for future
        self.db_manager.add_title(title)
        self._titles.append(title)
        self._index_single_title(title)
        
        return {
            "similarity_score": round(similarity_score, 4),
            "verification_probability": round(probability, 4),
            "violations": violations,
            "similar_titles": similar_titles,
        }
