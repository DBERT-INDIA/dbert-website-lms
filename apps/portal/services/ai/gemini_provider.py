import requests
import json
import time
from typing import List, Dict, Any, Generator, Optional
from .exceptions import *
from .schemas import GeminiResponse
from .telemetry import track_generation
from .model_registry import get_fallback_chain

class GeminiProvider:
    """Robust provider for Google Gemini API interactions."""
    
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:{action}"
    
    def __init__(self, api_key: Optional[str] = None, available_models: List[str] = None):
        import os
        if not api_key:
            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                keys = [k.strip() for k in os.environ.get("GEMINI_API_KEYS", "").split(",") if k.strip()]
                if keys:
                    api_key = keys[0]
        self.api_key = api_key
        self.available_models = available_models
        
    def _make_request(self, model: str, body: Dict[str, Any], stream: bool = False, timeout: int = 30) -> requests.Response:
        if not self.api_key:
            raise GeminiAuthError("No Gemini API key configured on client or server.")
        action = "streamGenerateContent?alt=sse" if stream else "generateContent"
        url = self.BASE_URL.format(model=model, action=action)
        
        try:
            r = requests.post(url, params={"key": self.api_key}, json=body, stream=stream, timeout=timeout)
            
            if r.status_code == 401 or r.status_code == 403:
                raise GeminiAuthError(f"Authentication failed for {model}: {r.text}")
            elif r.status_code == 404:
                raise GeminiModelRetiredError(f"Model {model} not found or retired: {r.text}")
            elif r.status_code == 429:
                raise GeminiRateLimitError(f"Rate limited on {model}")
            elif r.status_code >= 500:
                raise GeminiProviderError(f"Server error on {model}: {r.status_code} {r.text}")
                
            r.raise_for_status()
            return r
            
        except requests.Timeout:
            raise GeminiTimeoutError(f"Timeout reaching {model}")
        except requests.RequestException as e:
            raise GeminiProviderError(f"Network error: {e}")
            
    def generate_content(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048, response_schema: Optional[Dict[str, Any]] = None) -> GeminiResponse:
        """Generates content trying the fallback chain until success."""
        chain = get_fallback_chain(self.available_models)
        
        gen_config = {
            "temperature": temperature,
            "maxOutputTokens": max_tokens
        }
        
        if response_schema:
            gen_config["responseMimeType"] = "application/json"
            gen_config["responseSchema"] = response_schema
            
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": gen_config
        }
        
        last_err = None
        for model in chain:
            start_ts = time.time()
            try:
                r = self._make_request(model, body, stream=False)
                latency = (time.time() - start_ts) * 1000
                
                data = r.json()
                text = ""
                if "candidates" in data and len(data["candidates"]) > 0:
                    parts = data["candidates"][0].get("content", {}).get("parts", [])
                    if parts:
                        text = parts[0].get("text", "")
                        
                usage = data.get("usageMetadata", {})
                in_tokens = usage.get("promptTokenCount", 0)
                out_tokens = usage.get("candidatesTokenCount", 0)
                
                track_generation(model, latency, in_tokens, out_tokens, "success")
                return GeminiResponse(text=text, input_tokens=in_tokens, output_tokens=out_tokens, model_used=model)
                
            except (GeminiAuthError, GeminiModelRetiredError) as e:
                # Fatal errors for this key
                raise
            except (GeminiRateLimitError, GeminiTimeoutError, GeminiProviderError) as e:
                track_generation(model, (time.time() - start_ts) * 1000, 0, 0, "failed")
                last_err = str(e)
                continue # Try next model
                
        return GeminiResponse(text=None, error=f"All models failed. Last error: {last_err}")
        
    def stream_content(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> Generator[str, None, None]:
        """Streams content yielding text chunks, using fallback chain."""
        chain = get_fallback_chain(self.available_models)
        
        body = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        for model in chain:
            try:
                r = self._make_request(model, body, stream=True)
                for line in r.iter_lines():
                    if line:
                        line_str = line.decode('utf-8')
                        if line_str.startswith('data: '):
                            chunk_data = line_str[6:]
                            try:
                                chunk_json = json.loads(chunk_data)
                                if "candidates" in chunk_json and len(chunk_json["candidates"]) > 0:
                                    parts = chunk_json["candidates"][0].get("content", {}).get("parts", [])
                                    if parts:
                                        yield parts[0].get("text", "")
                            except json.JSONDecodeError:
                                pass
                return # Successfully streamed from this model, exit
            except (GeminiAuthError, GeminiModelRetiredError):
                raise
            except (GeminiRateLimitError, GeminiTimeoutError, GeminiProviderError):
                continue # Try next model on failure
                
        yield "Error: Could not generate response from any available AI models."


    def generate_embeddings(self, texts: List[str], model: str = "text-embedding-004") -> List[List[float]]:
        """Generates embeddings for a batch of texts."""
        if not self.api_key:
            return []
        url = self.BASE_URL.format(model=model, action="batchEmbedContents")
        
        requests_payload = [
            {"model": f"models/{model}", "content": {"parts": [{"text": text}]}}
            for text in texts
        ]
        
        body = {"requests": requests_payload}
        
        try:
            r = requests.post(url, params={"key": self.api_key}, json=body, timeout=30)
            if r.status_code == 401 or r.status_code == 403:
                raise GeminiAuthError(f"Authentication failed for {model}: {r.text}")
            elif r.status_code == 429:
                raise GeminiRateLimitError(f"Rate limited on {model}")
            r.raise_for_status()
            
            data = r.json()
            embeddings = []
            for item in data.get("embeddings", []):
                embeddings.append(item.get("values", []))
                
            return embeddings
        except requests.RequestException as e:
            raise GeminiProviderError(f"Embedding error: {e}")
