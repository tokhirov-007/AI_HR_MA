import spacy
import re
from typing import List, Set, Dict

class SkillExtractor:
    def __init__(self, model: str = "en_core_web_sm"):
        # Auto-download model if missing
        if not spacy.util.is_package(model):
            print(f"Downloading Spacy model '{model}'...")
            spacy.cli.download(model)
        
        print(f"Loading Spacy model '{model}'...")
        self.nlp = spacy.load(model)

        # Extended explicit skills list (Common Tech Stack)
        self.common_skills = {
            # Languages
            "python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin",
            # Frontend
            "react", "vue", "angular", "svelte", "next.js", "nuxt.js", "html", "css", "sass", "less", "tailwind",
            # Backend
            "node.js", "express", "nest.js", "django", "flask", "fastapi", "spring boot", "laravel", "rails", ".net",
            # Data / AI
            "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
            "machine learning", "deep learning", "nlp", "computer vision", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "opencv", "llm", "transformers", "hugging face",
            # DevOps / Cloud
            "docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible", "jenkins", "gitlab ci", "circleci",
            "git", "linux", "bash", "powershell",
            # Architecture / Concepts
            "rest api", "graphql", "grpc", "microservices", "event-driven architecture", "tdd", "bdd",
            "agile", "scrum", "kanban", "jira", "confluence"
        }

    def extract(self, text: str) -> Dict[str, List[str]]:
        """
        Extracts explicit skills and candidate noun chunks for semantic analysis.
        """
        if not text:
            return {"explicit": [], "candidates": []}

        doc = self.nlp(text)
        
        explicit_skills = self._find_explicit_skills(text)
        
        # Extract Noun Chunks for semantic mapping (e.g. "modern web frameworks")
        # Filter: 
        # 1. 2-5 words (excludes simple single words already caught or too long sentences)
        # 2. Not purely stop words
        candidates = []
        for chunk in doc.noun_chunks:
            clean_chunk = chunk.text.strip().lower()
            word_count = len(clean_chunk.split())
            
            if 1 <= word_count <= 5 and clean_chunk not in explicit_skills:
                candidates.append(chunk.text.strip())

        return {
            "explicit": list(explicit_skills),
            "candidates": list(set(candidates)) # Deduplicate
        }

    def _find_explicit_skills(self, text: str) -> Set[str]:
        found = set()
        text_lower = text.lower()
        
        for skill in self.common_skills:
            # Handle special characters in skills (C++, C#, .js)
            # We escape the skill for regex, but we must be careful with word boundaries
            
            pattern = None
            if any(c in skill for c in "+#."):
                # For C++, .NET, Node.js - exact substring match usually works better than naive ID regex
                # but we want to avoid "node.json" matching "node.js" if possible. 
                # Let's use simple boundary checks manually or regex with escape.
                pattern = re.escape(skill)
            else:
                # Strict word boundary for normal words "java", "go" (avoid "mongo")
                pattern = r'\b' + re.escape(skill) + r'\b'
            
            if re.search(pattern, text_lower):
                found.add(skill)
                
        return found
