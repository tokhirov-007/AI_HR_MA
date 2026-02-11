from app.question_engine.schemas import Question, QuestionType, DifficultyLevel
from typing import List, Dict

class QuestionBank:
    """
    Structured question database organized by skill, difficulty, and type.
    """
    
    def __init__(self):
        self.questions: List[Question] = self._initialize_questions()
        self._build_indexes()
    
    def _initialize_questions(self) -> List[Question]:
        """Initialize the question bank with pre-defined questions"""
        questions = []
        
        # Python Questions
        questions.extend([
            Question(
                id=1, skill="python", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое list comprehension в Python и когда его использовать?",
                expected_topics=["list comprehension", "syntax", "performance"]
            ),
            Question(
                id=2, skill="python", difficulty=DifficultyLevel.EASY, type=QuestionType.CASE,
                question="Напишите функцию, которая находит все уникальные элементы в списке.",
                expected_topics=["set", "list", "uniqueness"]
            ),
            Question(
                id=3, skill="python", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.THEORY,
                question="Объясните разницу между @staticmethod и @classmethod.",
                expected_topics=["decorators", "methods", "OOP"]
            ),
            Question(
                id=4, skill="python", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как бы вы оптимизировали код, который обрабатывает большой CSV файл?",
                expected_topics=["generators", "memory", "performance"]
            ),
            Question(
                id=5, skill="python", difficulty=DifficultyLevel.HARD, type=QuestionType.THEORY,
                question="Объясните работу GIL (Global Interpreter Lock) и его влияние на многопоточность.",
                expected_topics=["GIL", "threading", "concurrency"]
            ),
            Question(
                id=6, skill="python", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте систему кэширования с TTL для API запросов.",
                expected_topics=["caching", "TTL", "design patterns"]
            ),
        ])
        
        # JavaScript Questions
        questions.extend([
            Question(
                id=7, skill="javascript", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое замыкание (closure) в JavaScript?",
                expected_topics=["closure", "scope", "functions"]
            ),
            Question(
                id=8, skill="javascript", difficulty=DifficultyLevel.EASY, type=QuestionType.CASE,
                question="Напишите функцию debounce для оптимизации поиска.",
                expected_topics=["debounce", "setTimeout", "optimization"]
            ),
            Question(
                id=9, skill="javascript", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.THEORY,
                question="Объясните разницу между Promise и async/await.",
                expected_topics=["promises", "async", "asynchronous"]
            ),
            Question(
                id=10, skill="javascript", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как бы вы оптимизировали работу асинхронных запросов в SPA?",
                expected_topics=["async", "promises", "performance"]
            ),
            Question(
                id=11, skill="javascript", difficulty=DifficultyLevel.HARD, type=QuestionType.THEORY,
                question="Объясните Event Loop и как работает очередь микрозадач.",
                expected_topics=["event loop", "microtasks", "macrotasks"]
            ),
            Question(
                id=12, skill="javascript", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте систему управления состоянием для большого приложения.",
                expected_topics=["state management", "architecture", "patterns"]
            ),
        ])
        
        # React Questions
        questions.extend([
            Question(
                id=13, skill="react", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое Virtual DOM и зачем он нужен?",
                expected_topics=["virtual DOM", "reconciliation", "performance"]
            ),
            Question(
                id=14, skill="react", difficulty=DifficultyLevel.EASY, type=QuestionType.CASE,
                question="Создайте простой компонент счётчика с useState.",
                expected_topics=["useState", "hooks", "state"]
            ),
            Question(
                id=15, skill="react", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.THEORY,
                question="Объясните useEffect и его зависимости.",
                expected_topics=["useEffect", "lifecycle", "dependencies"]
            ),
            Question(
                id=16, skill="react", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как избежать лишних ререндеров в React?",
                expected_topics=["memo", "useMemo", "useCallback", "optimization"]
            ),
            Question(
                id=17, skill="react", difficulty=DifficultyLevel.HARD, type=QuestionType.THEORY,
                question="Объясните работу React Fiber и приоритизацию рендеринга.",
                expected_topics=["fiber", "concurrent mode", "scheduling"]
            ),
            Question(
                id=18, skill="react", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте архитектуру для микрофронтенд приложения на React.",
                expected_topics=["microfrontends", "architecture", "module federation"]
            ),
        ])
        
        # Node.js Questions
        questions.extend([
            Question(
                id=19, skill="node.js", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое middleware в Express.js?",
                expected_topics=["middleware", "express", "request pipeline"]
            ),
            Question(
                id=20, skill="node.js", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как организовать обработку ошибок в Express приложении?",
                expected_topics=["error handling", "middleware", "try-catch"]
            ),
            Question(
                id=21, skill="node.js", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте систему обработки очередей с использованием Node.js.",
                expected_topics=["queues", "workers", "scalability"]
            ),
        ])
        
        # Django Questions
        questions.extend([
            Question(
                id=22, skill="django", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое ORM в Django и как он работает?",
                expected_topics=["ORM", "models", "database"]
            ),
            Question(
                id=23, skill="django", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как оптимизировать запросы к базе данных в Django?",
                expected_topics=["select_related", "prefetch_related", "N+1 problem"]
            ),
            Question(
                id=24, skill="django", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте систему прав доступа для многопользовательского приложения.",
                expected_topics=["permissions", "authentication", "authorization"]
            ),
        ])
        
        # Database Questions
        questions.extend([
            Question(
                id=25, skill="postgresql", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое индексы и зачем они нужны?",
                expected_topics=["indexes", "performance", "queries"]
            ),
            Question(
                id=26, skill="postgresql", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как бы вы оптимизировали медленный SQL запрос?",
                expected_topics=["EXPLAIN", "indexes", "query optimization"]
            ),
            Question(
                id=27, skill="sql", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Объясните разницу между INNER JOIN и LEFT JOIN.",
                expected_topics=["joins", "SQL", "relationships"]
            ),
        ])
        
        # Docker Questions
        questions.extend([
            Question(
                id=28, skill="docker", difficulty=DifficultyLevel.EASY, type=QuestionType.THEORY,
                question="Что такое Docker контейнер и чем он отличается от виртуальной машины?",
                expected_topics=["containers", "virtualization", "isolation"]
            ),
            Question(
                id=29, skill="docker", difficulty=DifficultyLevel.MEDIUM, type=QuestionType.CASE,
                question="Как организовать multi-stage build для оптимизации Docker образа?",
                expected_topics=["multi-stage", "optimization", "Dockerfile"]
            ),
            Question(
                id=30, skill="docker", difficulty=DifficultyLevel.HARD, type=QuestionType.CASE,
                question="Спроектируйте Docker Compose конфигурацию для микросервисной архитектуры.",
                expected_topics=["docker-compose", "microservices", "networking"]
            ),
        ])
        
        return questions
    
    def _build_indexes(self):
        """Build indexes for fast lookup"""
        self.by_skill: Dict[str, List[Question]] = {}
        self.by_difficulty: Dict[DifficultyLevel, List[Question]] = {}
        self.by_type: Dict[QuestionType, List[Question]] = {}
        
        for question in self.questions:
            # Index by skill
            skill_lower = question.skill.lower()
            if skill_lower not in self.by_skill:
                self.by_skill[skill_lower] = []
            self.by_skill[skill_lower].append(question)
            
            # Index by difficulty
            if question.difficulty not in self.by_difficulty:
                self.by_difficulty[question.difficulty] = []
            self.by_difficulty[question.difficulty].append(question)
            
            # Index by type
            if question.type not in self.by_type:
                self.by_type[question.type] = []
            self.by_type[question.type].append(question)
    
    def get_questions_by_skill(self, skill: str) -> List[Question]:
        """Get all questions for a specific skill"""
        return self.by_skill.get(skill.lower(), [])
    
    def get_questions_by_skill_and_difficulty(
        self, 
        skill: str, 
        difficulty: DifficultyLevel
    ) -> List[Question]:
        """Get questions filtered by skill and difficulty"""
        skill_questions = self.get_questions_by_skill(skill)
        return [q for q in skill_questions if q.difficulty == difficulty]
    
    def get_questions_by_skill_difficulty_type(
        self,
        skill: str,
        difficulty: DifficultyLevel,
        question_type: QuestionType
    ) -> List[Question]:
        """Get questions filtered by skill, difficulty, and type"""
        questions = self.get_questions_by_skill_and_difficulty(skill, difficulty)
        return [q for q in questions if q.type == question_type]
