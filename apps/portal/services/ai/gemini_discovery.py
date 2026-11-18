"""
services/ai/gemini_discovery.py - Unified Dynamic Gemini Model Discovery Engine ('One Mech')

Eliminates hardcoded model strings by:
1. Dynamically fetching all available models for any provided API key from Google's Model API.
2. Filtering for models supporting 'generateContent'.
3. Discarding audio, image, embedding, and non-text models.
4. Intelligently ranking models: latest Flash -> Pro -> compatible fallback.
5. Caching verified model capabilities to minimize network latency (1-hour TTL per key hash).
"""

import hashlib
import json
import logging
import os
import re
import time
from typing import Dict, List, Optional, Tuple
import requests

logger = logging.getLogger("dbert.ai.discovery")

# In-memory cache: {key_hash: (timestamp, default_model, available_models_list)}
_MODEL_CACHE: Dict[str, Tuple[float, str, List[str]]] = {}
CACHE_TTL_SECONDS = 3600  # 1 hour

NON_TEXT_KEYWORDS = (
    "tts", "audio", "image", "imagen", "transcribe", "clip", "lyria",
    "robotics", "computer-use", "customtools", "embedding", "aqa"
)


def _hash_key(api_key: str) -> str:
    """Generate SHA-256 hash of API key for safe cache keys and log sanitization."""
    return hashlib.sha256(api_key.strip().encode("utf-8")).hexdigest()


def _extract_model_version(model_name: str) -> float:
    """Extract numeric version from model name for semantic sorting (e.g. 'gemini-2.0-flash' -> 2.0)."""
    clean = model_name.lower()
    match = re.search(r"(\d+(?:\.\d+)?)", clean)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    if "latest" in clean:
        return 2.5
    return 0.0


def _rank_models(model_names: List[str]) -> Tuple[Optional[str], List[str]]:
    """
    Ranks valid text generation models dynamically without hardcoding:
    1. Stable Flash models prioritized (fastest & cost-effective for tutoring & tasks), sorted by version descending.
    2. Preview/experimental Flash models.
    3. Stable Pro models, sorted by version descending.
    4. Preview/experimental Pro models.
    5. Any other text generation models.
    """
    flash_models = []
    pro_models = []
    other_models = []

    for name in model_names:
        clean = name.replace("models/", "").strip()
        lower = clean.lower()

        # Discard deprecated 1.0 generation or vision models
        if "1.0" in lower or "vision" in lower:
            continue

        version = _extract_model_version(clean)
        is_experimental = 1 if ("exp" in lower or "preview" in lower or "8b" in lower or "customtools" in lower) else 0

        if "flash" in lower:
            flash_models.append((version, is_experimental, clean))
        elif "pro" in lower:
            pro_models.append((version, is_experimental, clean))
        else:
            other_models.append((version, is_experimental, clean))

    # Sort descending by version, with non-experimental preferred (is_experimental == 0 first)
    flash_sorted = [item[2] for item in sorted(flash_models, key=lambda x: (-x[1], x[0]), reverse=True)]
    pro_sorted = [item[2] for item in sorted(pro_models, key=lambda x: (-x[1], x[0]), reverse=True)]
    other_sorted = [item[2] for item in sorted(other_models, key=lambda x: (-x[1], x[0]), reverse=True)]

    ordered = flash_sorted + pro_sorted + other_sorted
    best_default = ordered[0] if ordered else None

    return best_default, ordered


def discover_gemini_models(
    api_key: Optional[str] = None,
    force_refresh: bool = False,
    timeout: int = 10
) -> Tuple[Optional[str], List[str], Optional[str]]:
    """
    Core 'One Mech' discovery function:
    Fetches available models from Google Generative Language API, filters, ranks, and returns:
    (best_default_model, ordered_available_models, error_message)
    """
    # Fallback to server key if none provided
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            keys = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", "").split(",") if k.strip()]
            if keys:
                api_key = keys[0]

    if not api_key:
        return None, [], "No Gemini API key provided or configured in server environment."

    clean_key = api_key.strip().strip('"\'`')
    if len(clean_key) < 15:
        return None, [], "The provided Gemini API key is too short or malformed."

    key_hash = _hash_key(clean_key)
    now = time.time()

    # Check cache if not forcing refresh
    if not force_refresh and key_hash in _MODEL_CACHE:
        cached_ts, cached_default, cached_models = _MODEL_CACHE[key_hash]
        if now - cached_ts < CACHE_TTL_SECONDS:
            return cached_default, cached_models, None

    # Fetch models from Google's Model API
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    headers = {"User-Agent": "DBERT-Dynamic-AI-Discovery/2.0"}

    try:
        r = requests.get(url, params={"key": clean_key}, headers=headers, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            raw_models = data.get("models", [])

            valid_names = []
            for m in raw_models:
                name = m.get("name", "")
                methods = m.get("supportedGenerationMethods", [])
                
                # Must support generateContent
                if "generateContent" not in methods:
                    continue

                # Filter out audio, image, embedding, robotics
                name_lower = name.lower()
                if any(kw in name_lower for kw in NON_TEXT_KEYWORDS):
                    continue

                valid_names.append(name)

            best_default, ordered_models = _rank_models(valid_names)

            if not ordered_models:
                # If Google returned no compatible generation models
                return None, [], "Key authenticated successfully, but no compatible text generation models were returned."

            # Update cache
            _MODEL_CACHE[key_hash] = (now, best_default, ordered_models)
            return best_default, ordered_models, None

        # Handle specific error status codes
        err_msg = ""
        try:
            err_json = r.json().get("error", {})
            err_msg = err_json.get("message", "")
        except Exception:
            pass

        if r.status_code in (400, 401, 403):
            return None, [], f"Google API authentication failed (HTTP {r.status_code}): {err_msg or 'Invalid API key.'}"
        elif r.status_code == 429:
            # If rate limited on discovery, check if we have any stale cache to salvage
            if key_hash in _MODEL_CACHE:
                _, cached_default, cached_models = _MODEL_CACHE[key_hash]
                return cached_default, cached_models, None
            return None, [], "Google Gemini rate limit exceeded during model discovery."
        else:
            return None, [], f"Google API returned error (HTTP {r.status_code}): {err_msg or r.text[:150]}"

    except requests.exceptions.Timeout:
        if key_hash in _MODEL_CACHE:
            _, cached_default, cached_models = _MODEL_CACHE[key_hash]
            return cached_default, cached_models, None
        return None, [], f"Connection timed out reaching Google Gemini API ({timeout}s limit)."
    except requests.exceptions.RequestException as e:
        if key_hash in _MODEL_CACHE:
            _, cached_default, cached_models = _MODEL_CACHE[key_hash]
            return cached_default, cached_models, None
        return None, [], f"Network error during model discovery: {e}"
    except Exception as e:
        return None, [], f"Unexpected error during model discovery: {e}"


def get_dynamic_fallback_chain(
    api_key: Optional[str] = None,
    user_models: Optional[List[str]] = None
) -> List[str]:
    """
    Returns an ordered list of model names to try for generation.
    If user_models is passed (e.g. from validated key session), ranks those.
    Otherwise queries discover_gemini_models.
    """
    if user_models:
        valid_cleaned = [
            m.replace("models/", "").strip() for m in user_models
            if isinstance(m, str) and not any(kw in m.lower() for kw in NON_TEXT_KEYWORDS)
        ]
        if valid_cleaned:
            _, ranked = _rank_models(valid_cleaned)
            # If the user models list starts with a verified working flash model, preserve it as first
            first_user_m = valid_cleaned[0]
            if first_user_m in (ranked or []) and "flash" in first_user_m.lower():
                ranked = [first_user_m] + [m for m in ranked if m != first_user_m]
            return ranked or valid_cleaned

    # Query dynamic discovery
    _, models, _ = discover_gemini_models(api_key=api_key)
    if models:
        return models

    # Safe dynamic fallback (using current stable aliases)
    return ["gemini-2.5-flash", "gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-pro"]


def get_default_model(api_key: Optional[str] = None) -> str:
    """Dynamically retrieves the optimal default model for the provided API key (or server key)."""
    best_default, _, _ = discover_gemini_models(api_key=api_key)
    return best_default or "gemini-2.5-flash"


def clear_model_cache():
    """Testing helper to clear in-memory model cache."""
    global _MODEL_CACHE
    _MODEL_CACHE.clear()
