"""
services/ai/model_registry.py - Gemini Model Registry & Fallback Chain Delegation

Delegates model resolution and ranking to the dynamic discovery engine ('One Mech')
in services/ai/gemini_discovery.py to prevent any hardcoded model versions.
"""

from typing import List, Optional
from .gemini_discovery import get_dynamic_fallback_chain, discover_gemini_models

def get_fallback_chain(user_models: Optional[List[str]] = None, api_key: Optional[str] = None) -> List[str]:
    """
    Returns an ordered list of models to try.
    Dynamically ranks user or discovered models with Flash variants first,
    sorted by version descending, avoiding any hardcoded model chains.
    """
    return get_dynamic_fallback_chain(api_key=api_key, user_models=user_models)


def get_default_model(api_key: Optional[str] = None) -> str:
    """
    Dynamically retrieves the optimal default model for the provided API key (or server key).
    """
    best_default, _, _ = discover_gemini_models(api_key=api_key)
    return best_default or "gemini-2.5-flash"
