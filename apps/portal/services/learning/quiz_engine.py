import json
import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

logger = logging.getLogger('quiz_engine')

class QuizOption(BaseModel):
    text: str = Field(..., min_length=1)

class QuizQuestion(BaseModel):
    id: int
    question: str = Field(..., min_length=10)
    options: List[str] = Field(..., min_length=4, max_length=5)
    correct_index: int = Field(..., ge=0)
    concept_id: Optional[str] = Field(default=None, description="The ID of the concept this question tests.")

    @model_validator(mode='after')
    def validate_options(self) -> 'QuizQuestion':
        if not (0 <= self.correct_index < len(self.options)):
            raise ValueError(f"correct_index {self.correct_index} is out of bounds for options array of size {len(self.options)}")
            
        unique_opts = set(self.options)
        if len(unique_opts) != len(self.options):
            raise ValueError("Duplicate options detected in question.")
            
        for opt in self.options:
            if not opt or not str(opt).strip():
                raise ValueError("Empty option text detected.")
                
        return self

class QuizSchema(BaseModel):
    questions: List[QuizQuestion] = Field(..., min_length=5, max_length=5)

    @model_validator(mode='after')
    def validate_unique_questions(self) -> 'QuizSchema':
        ids = set(q.id for q in self.questions)
        if len(ids) != len(self.questions):
            raise ValueError("Question IDs must be unique.")
            
        texts = set(q.question for q in self.questions)
        if len(texts) != len(self.questions):
            raise ValueError("Duplicate questions detected.")
            
        return self

class QuizEngine:
    @staticmethod
    def generate_quiz(provider, course_title: str, chapter_title: str, day_number: int, topics_summary: str, max_retries: int = 3) -> Optional[List[Dict[str, Any]]]:
        from services.ai.gemini_provider import GeminiProviderError
        
        prompt = (
            f"Generate a rigorous 5-question multiple choice quiz for Day {day_number} of '{course_title}' (Chapter: {chapter_title}).\\n"
            f"Topics Covered: {topics_summary}\\n\\n"
            "Return ONLY a valid JSON array of EXACTLY 5 objects, with NO markdown surrounding it.\\n"
            "Each object MUST have this schema:\\n"
            "{\\n"
            '  "id": 1,\\n'
            '  "question": "What is ...?",\\n'
            '  "options": ["Option A", "Option B", "Option C", "Option D"],\\n'
            '  "correct_index": 0\\n'
            "}\\n"
            "Ensure options are unique, and the correct_index strictly matches the zero-based position of the correct answer."
        )

        for attempt in range(max_retries):
            try:
                # Use strict structured outputs using the provider
                raw_res = provider.generate_content_sync(prompt, temperature=0.2, response_schema=QuizSchema.model_json_schema())
                if not raw_res:
                    continue
                    
                cleaned = raw_res.strip()
                if cleaned.startswith("`"):
                    cleaned = cleaned.split("\\n", 1)[-1].rsplit("`", 1)[0].strip()
                    
                data = json.loads(cleaned)
                
                # In structured outputs, the root might be an object containing 'questions', or directly an array if Gemini ignored schema root
                if isinstance(data, list):
                    data = {"questions": data}
                    
                validated = QuizSchema.model_validate(data)
                return [q.model_dump() for q in validated.questions]
            except Exception as e:
                logger.error(f"Quiz generation failed on attempt {attempt+1}: {e}")
                
        return None

