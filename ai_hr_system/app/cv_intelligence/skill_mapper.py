import os
import logging
from sentence_transformers import SentenceTransformer, util
import torch

# Suppress noisy transformers logging
logging.getLogger("transformers").setLevel(logging.ERROR)

class SkillMapper:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        # Check if we can run offline or need to download
        # SentenceTransformer handles downloading automatically to cache
        print(f"Loading Semantic Model '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        
        # Knowledge Base: Abstract/Vague term -> Concrete Skills
        # This acts as the "AI Interpretation" layer
        self.ontology = {
            "modern javascript": ["ES6+", "Async/Await", "React", "Vue", "Angular", "TypeScript"],
            "modern js": ["ES6+", "React", "Vue", "Angular"],
            "modern frontend frameworks": ["React", "Vue", "Angular", "Svelte"],
            "modern backend frameworks": ["Django", "FastAPI", "NestJS", "Spring Boot"],
            "full stack": ["Frontend Development", "Backend Development", "Database Management", "API Integration"],
            "fullstack": ["Frontend Development", "Backend Development", "Database Management"],
            "backend experience": ["Rest API", "Database Design", "Authentication", "System Architecture", "Caching"],
            "frontend experience": ["UI/UX Implementation", "Responsive Design", "State Management", "Component Architecture"],
            "cloud native": ["Microservices", "Docker", "Kubernetes", "AWS", "CI/CD"],
            "data science stack": ["Python", "Pandas", "NumPy", "Scikit-Learn", "Jupyter"],
            "big data": ["Hadoop", "Spark", "Kafka", "Data Lakes"]
        }
        
        # Pre-compute embeddings for ontology keys for speed
        self.ontology_keys = list(self.ontology.keys())
        self.ontology_embeddings = self.model.encode(self.ontology_keys, convert_to_tensor=True)

    def map_skills(self, candidates: list[str]) -> list[str]:
        """
        Maps candidate phrases (e.g., "experienced in modern js") to concrete skills.
        """
        inferred = set()
        
        if not candidates:
            return []

        # Encode candidates
        # Batch encode is efficient
        candidate_embeddings = self.model.encode(candidates, convert_to_tensor=True)
        
        # Compute Cosine Similarity
        cosine_scores = util.cos_sim(candidate_embeddings, self.ontology_embeddings)
        
        # Threshold: How close must the phrase be? 
        # "modern javascript" vs "modern javascript" = 1.0
        # "modern js features" vs "modern javascript" ~ 0.8
        # "java" vs "modern javascript" ~ low
        THRESHOLD = 0.65
        
        # cosine_scores is [num_candidates, num_ontology_keys]
        for i in range(len(candidates)):
            scores = cosine_scores[i]
            best_score_idx = torch.argmax(scores).item()
            best_score = scores[best_score_idx].item()
            
            if best_score >= THRESHOLD:
                matched_concept = self.ontology_keys[best_score_idx]
                # print(f"DEBUG: Mapped '{candidates[i]}' -> '{matched_concept}' ({best_score:.2f})")
                inferred.update(self.ontology[matched_concept])
                
        return list(inferred)
