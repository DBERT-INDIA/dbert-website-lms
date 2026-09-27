import yaml
import json
import uuid
import logging
from typing import Dict, Any

logger = logging.getLogger('course_ingestion')

class CourseIngester:
    @staticmethod
    def ingest_manifest(conn, manifest_path: str, provider) -> bool:
        '''
        Parses canonical course YAML manifest, chunks contents, gets embeddings via Gemini,
        and saves to gl_course_chunks.
        '''
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load manifest {manifest_path}: {e}")
            return False

        course_id = manifest.get('course_id')
        version = manifest.get('version', '1.0')
        
        if not course_id:
            logger.error("Manifest missing course_id")
            return False

        chunks_to_insert = []
        texts_to_embed = []
        
        for module in manifest.get('modules', []):
            mod_id = module.get('id')
            
            # Module-level resources
            for res in module.get('resources', []):
                text_content = res.get('text', '')
                if not text_content: continue
                texts_to_embed.append(text_content)
                chunks_to_insert.append({
                    "chunk_id": str(uuid.uuid4()),
                    "course_id": course_id,
                    "course_version": version,
                    "module_id": mod_id,
                    "concept_id": None,
                    "subtopic_id": None,
                    "difficulty": module.get('difficulty', 1),
                    "content_type": res.get('type', 'resource'),
                    "source": res.get('source', 'module'),
                    "text_content": text_content
                })

            # Concept-level resources
            for concept in module.get('concepts', []):
                c_id = concept.get('id')
                for res in concept.get('resources', []):
                    text_content = res.get('text', '')
                    if not text_content: continue
                    texts_to_embed.append(text_content)
                    chunks_to_insert.append({
                        "chunk_id": str(uuid.uuid4()),
                        "course_id": course_id,
                        "course_version": version,
                        "module_id": mod_id,
                        "concept_id": c_id,
                        "subtopic_id": None,
                        "difficulty": concept.get('difficulty', 1),
                        "content_type": res.get('type', 'concept_resource'),
                        "source": res.get('source', 'concept'),
                        "text_content": text_content
                    })

        if not texts_to_embed:
            return True

        # Generate embeddings in batch
        try:
            embeddings = provider.generate_embeddings(texts_to_embed)
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            return False

        # Save to DB
        for i, chunk in enumerate(chunks_to_insert):
            chunk["embedding_json"] = json.dumps(embeddings[i])
            
            conn.execute(
                '''INSERT INTO gl_course_chunks (
                    chunk_id, course_id, course_version, module_id, concept_id,
                    subtopic_id, difficulty, content_type, source, text_content,
                    embedding_json, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))''',
                (
                    chunk["chunk_id"], chunk["course_id"], chunk["course_version"],
                    chunk["module_id"], chunk["concept_id"], chunk["subtopic_id"],
                    chunk["difficulty"], chunk["content_type"], chunk["source"],
                    chunk["text_content"], chunk["embedding_json"]
                )
            )
            
        conn.commit()
        return True
