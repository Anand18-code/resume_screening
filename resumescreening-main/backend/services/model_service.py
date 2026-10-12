"""Model management and inference service.

Handles loading cached machine learning pipelines (Job Category Classifier and
Candidate Fit Model) and performing predictions.
"""

import os
from typing import Any, Dict, Optional, Tuple
import joblib

from backend.utils.preprocessing import clean_text

# Locate the models directory relative to this service file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
MODELS_DIR = os.path.join(BACKEND_DIR, "models")


class ModelService:
    """Singleton service for loading and executing ML models."""
    
    _instance: Optional["ModelService"] = None
    
    def __new__(cls) -> "ModelService":
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
            cls._instance._category_model = None
            cls._instance._screening_model = None
            cls._instance._load_all_models()
        return cls._instance

    def _find_model_path(self, model_name: str) -> Optional[str]:
        """Searches for model file across standard project locations."""
        candidates = [
            os.path.join(MODELS_DIR, model_name),
            os.path.join(BACKEND_DIR, model_name),
            os.path.join(os.path.dirname(BACKEND_DIR), "models", model_name),
            os.path.join(os.path.dirname(BACKEND_DIR), model_name)
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def _load_all_models(self) -> None:
        """Loads available model pipelines into memory."""
        # 1. Job Category Classification Model
        cat_path = self._find_model_path("category_model.pkl")
        if cat_path:
            try:
                self._category_model = joblib.load(cat_path)
            except Exception as e:
                print(f"[WARN] Failed to load category model from {cat_path}: {e}")
                self._category_model = None

        # 2. Screening Recommendation Model (if present)
        scr_path = self._find_model_path("screening_model.pkl")
        if scr_path:
            try:
                self._screening_model = joblib.load(scr_path)
            except Exception as e:
                print(f"[WARN] Failed to load screening model from {scr_path}: {e}")
                self._screening_model = None

    @property
    def category_model_loaded(self) -> bool:
        return self._category_model is not None

    @property
    def models_directory(self) -> str:
        return MODELS_DIR

    def predict_category(self, text: str) -> Tuple[str, str, Optional[float]]:
        """Predicts the professional job domain category for a resume.
        
        Args:
            text: Raw or cleaned resume text.
            
        Returns:
            Tuple of (predicted_category, method_used, confidence_score)
        """
        cleaned = clean_text(text)
        if not cleaned:
            return "General Profile", "Heuristic Default", 50.0

        if self._category_model is not None:
            try:
                prediction = self._category_model.predict([cleaned])[0]
                # If model supports predict_proba, get top probability
                confidence = None
                if hasattr(self._category_model, "predict_proba"):
                    try:
                        probs = self._category_model.predict_proba([cleaned])[0]
                        confidence = round(float(max(probs)) * 100.0, 1)
                    except Exception:
                        confidence = 95.0
                return str(prediction), "NLP Classifier (TF-IDF + Logistic Regression)", confidence
            except Exception as e:
                print(f"[WARN] Category prediction error: {e}")

        # Fallback heuristic based on prominent domain keywords
        lowered = cleaned.lower()
        if any(w in lowered for w in ["data science", "machine learning", "pytorch", "tensorflow", "deep learning"]):
            return "Data Science", "Keyword Heuristic Fallback", 85.0
        elif any(w in lowered for w in ["react", "frontend", "javascript", "typescript", "html", "css"]):
            return "Web Designing / Frontend", "Keyword Heuristic Fallback", 85.0
        elif any(w in lowered for w in ["devops", "kubernetes", "docker", "ci/cd", "terraform", "aws"]):
            return "DevOps Engineer", "Keyword Heuristic Fallback", 85.0
        elif any(w in lowered for w in ["java", "spring boot", "microservices"]):
            return "Java Developer", "Keyword Heuristic Fallback", 85.0
        elif any(w in lowered for w in ["python", "django", "fastapi", "flask"]):
            return "Python Developer", "Keyword Heuristic Fallback", 85.0

        return "Software Engineering", "Keyword Heuristic Fallback", 75.0


# Global service instance
model_service = ModelService()
