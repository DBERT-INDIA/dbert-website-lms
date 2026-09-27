from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class GeminiMessage:
    role: str
    content: str

@dataclass
class GeminiResponse:
    text: Optional[str]
    input_tokens: int = 0
    output_tokens: int = 0
    model_used: str = ""
    cached: bool = False
    error: Optional[str] = None
