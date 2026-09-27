import numpy as np
import json
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger('rag_retriever')

class RAGRetriever:
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
            return 0.0
        return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

    @staticmethod
    def retrieve_chunks(
        conn,
        query_embedding: List[float],
        course_id: Optional[int] = None,
        concept_id: Optional[str] = None,
        top_k: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        '''
        Student-aware retrieval. Filters chunks based on course and concept,
        then performs in-memory cosine similarity search.
        '''
        query = "SELECT * FROM gl_course_chunks WHERE 1=1"
        params = []
        
        if course_id is not None:
            query += " AND course_id = ?"
            params.append(course_id)
            
        if concept_id is not None:
            query += " AND (concept_id = ? OR concept_id IS NULL)"
            params.append(concept_id)
            
        rows = conn.execute(query, tuple(params)).fetchall()

        results = []
        for row in rows:
            try:
                emb = json.loads(row['embedding_json'])
                score = RAGRetriever._cosine_similarity(query_embedding, emb)
                if score >= threshold:
                    results.append({
                        "chunk_id": row["chunk_id"],
                        "concept_id": row["concept_id"],
                        "content_type": row["content_type"],
                        "text_content": row["text_content"],
                        "source": row["source"],
                        "similarity": score
                    })
            except Exception as e:
                logger.error(f"Error parsing embedding for chunk {row['chunk_id']}: {e}")

        # Sort by highest similarity
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
