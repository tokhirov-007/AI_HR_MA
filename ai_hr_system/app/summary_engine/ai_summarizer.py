from app.cv_intelligence.schemas import CVAnalysisResult
from typing import List

class AISummarizer:
    """
    Generates HR-friendly and Technical summaries from CV analysis results.
    """
    
    def __init__(self):
        # Skill categories for better summarization
        self.skill_categories = {
            "frontend": ["react", "vue", "angular", "svelte", "html", "css", "javascript", "typescript", 
                        "next.js", "nuxt.js", "tailwind", "sass", "less"],
            "backend": ["node.js", "express", "nest.js", "django", "flask", "fastapi", "spring boot", 
                       "laravel", "rails", ".net", "python", "java", "go", "rust", "php", "ruby"],
            "database": ["sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra"],
            "ai_ml": ["machine learning", "deep learning", "nlp", "computer vision", "tensorflow", 
                     "pytorch", "scikit-learn", "pandas", "numpy", "opencv", "llm", "transformers"],
            "devops": ["docker", "kubernetes", "aws", "azure", "gcp", "terraform", "ansible", 
                      "jenkins", "gitlab ci", "circleci", "git", "linux", "bash"],
        }
    
    def generate_hr_summary(self, cv_result: CVAnalysisResult) -> str:
        """
        Generate concise HR-friendly summary.
        Example: "Кандидат имеет 3 года опыта в JavaScript, React и Node.js, 
                  участвовал в full-stack проектах."
        """
        skills = cv_result.skills_detected + cv_result.inferred_skills
        skills_unique = list(set(skills))[:5]  # Top 5 unique skills
        
        years = cv_result.experience_years or 0
        years_text = f"{int(years)} года" if years else "опыт"
        
        # Detect role type
        role_type = self._detect_role_type(skills_unique)
        
        skills_text = ", ".join(skills_unique[:3])
        
        summary = f"Кандидат имеет {years_text} опыта в {skills_text}"
        
        if role_type:
            summary += f", работал в {role_type} проектах"
        
        if len(skills_unique) > 3:
            summary += f", владеет {len(skills_unique)} технологиями"
        
        summary += "."
        
        return summary
    
    def generate_technical_summary(self, cv_result: CVAnalysisResult) -> str:
        """
        Generate detailed technical summary.
        Example: "3 года опыта, фронтенд: React 18, Vue 3, backend: Node.js + PostgreSQL, 
                  знает CI/CD, REST API."
        """
        skills = cv_result.skills_detected + cv_result.inferred_skills
        skills_unique = list(set([s.lower() for s in skills]))
        
        years = cv_result.experience_years or 0
        
        # Categorize skills
        categorized = self._categorize_skills(skills_unique)
        
        parts = []
        
        if years:
            parts.append(f"{int(years)} года опыта")
        
        if categorized.get("frontend"):
            frontend_skills = ", ".join(categorized["frontend"][:3])
            parts.append(f"фронтенд: {frontend_skills}")
        
        if categorized.get("backend"):
            backend_skills = ", ".join(categorized["backend"][:3])
            parts.append(f"backend: {backend_skills}")
        
        if categorized.get("database"):
            db_skills = ", ".join(categorized["database"][:2])
            parts.append(f"БД: {db_skills}")
        
        if categorized.get("ai_ml"):
            ai_skills = ", ".join(categorized["ai_ml"][:2])
            parts.append(f"AI/ML: {ai_skills}")
        
        if categorized.get("devops"):
            devops_skills = ", ".join(categorized["devops"][:2])
            parts.append(f"DevOps: {devops_skills}")
        
        summary = ", ".join(parts) + "."
        
        return summary
    
    def _categorize_skills(self, skills: List[str]) -> dict:
        """Categorize skills into frontend, backend, etc."""
        categorized = {}
        
        for category, category_skills in self.skill_categories.items():
            matched = [s for s in skills if s.lower() in category_skills]
            if matched:
                categorized[category] = matched
        
        return categorized
    
    def _detect_role_type(self, skills: List[str]) -> str:
        """Detect if candidate is full-stack, frontend, backend, etc."""
        skills_lower = [s.lower() for s in skills]
        
        has_frontend = any(s in self.skill_categories["frontend"] for s in skills_lower)
        has_backend = any(s in self.skill_categories["backend"] for s in skills_lower)
        
        if has_frontend and has_backend:
            return "full-stack"
        elif has_frontend:
            return "frontend"
        elif has_backend:
            return "backend"
        
        return ""
