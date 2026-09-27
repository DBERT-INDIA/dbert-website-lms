from typing import List

# Current official Gemini baseline
PRIMARY_MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"
OPTIONAL_MODEL = "gemini-3.7-flash"

def get_fallback_chain(user_models: List[str] = None) -> List[str]:
    """Returns an ordered list of models to try, based on user capabilities."""
    chain = []
    
    # If the user has a specific subset of models (BYOK), prioritize what's available
    if user_models:
        if PRIMARY_MODEL in user_models:
            chain.append(PRIMARY_MODEL)
        elif OPTIONAL_MODEL in user_models:
            chain.append(OPTIONAL_MODEL)
        if FALLBACK_MODEL in user_models:
            chain.append(FALLBACK_MODEL)
            
        # Fallback to whatever they have if our baseline isn't there
        for m in user_models:
            if m not in chain:
                chain.append(m)
    else:
        # Server default fallback chain
        chain = [PRIMARY_MODEL, OPTIONAL_MODEL, FALLBACK_MODEL]
        
    return chain
