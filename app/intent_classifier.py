"""
intent_classifier.py – TF-IDF based intent classification
Trained on voyago_dataset.csv at startup (no external model download needed)
"""

import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pickle
import os
from app.config import settings


class IntentClassifier:
    """
    Lightweight TF-IDF + Logistic Regression classifier.
    Trains in < 1 second on the 5000-row dataset.
    Supports Arabic + English mixed text.
    """

    def __init__(self):
        self.model: Pipeline | None = None
        self.label_map: dict = {}
        self._load_or_train()

    # ── Text normalisation ────────────────────────────────────────────────
    @staticmethod
    def normalize(text: str) -> str:
        text = text.lower().strip()
        # Remove Arabic diacritics (tashkeel)
        text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
        # Normalize alef variants
        text = re.sub(r"[أإآ]", "ا", text)
        # Normalize teh marbuta
        text = re.sub(r"ة", "ه", text)
        # Remove punctuation
        text = re.sub(r"[^\w\s]", " ", text)
        return text

    # ── Training ──────────────────────────────────────────────────────────
    def _train(self, df: pd.DataFrame):
        X = df["User_Query_Normalized"].fillna("").apply(self.normalize)
        y = df["Intent"]

        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(
                analyzer="char_wb",
                ngram_range=(2, 5),
                max_features=20_000,
                sublinear_tf=True,
            )),
            ("clf", LogisticRegression(
                max_iter=1000,
                C=5.0,
                class_weight="balanced",
                solver="lbfgs",
            )),
        ])
        self.model.fit(X, y)

    def _load_or_train(self):
        cache = "data/intent_model.pkl"
        if os.path.exists(cache):
            with open(cache, "rb") as f:
                self.model = pickle.load(f)
            print("[IntentClassifier] Loaded cached model.")
        else:
            print("[IntentClassifier] Training model …")
            df = pd.read_csv(settings.DATASET_PATH)
            self._train(df)
            os.makedirs("data", exist_ok=True)
            with open(cache, "wb") as f:
                pickle.dump(self.model, f)
            print("[IntentClassifier] Model trained and cached.")

    # ── Prediction ────────────────────────────────────────────────────────
    def predict(self, text: str) -> tuple[str, float]:
        """
        Returns (intent_label, confidence_score 0-1).
        """
        if self.model is None:
            return "unknown", 0.0

        normalized = self.normalize(text)
        tokens = set(normalized.split())

        # ── Rule-based overrides: natural conversational Arabic & English ────

        # Hotels — حجز / إقامة / نوم
        hotel_keywords = {
            "فندق", "فنادق", "hotel", "hotels", "اقامه", "اقامة",
            "احجز", "حجز", "حجزت", "انام", "بيت", "شاليه", "ريزورت",
            "resort", "lodge", "inn", "book", "booking", "room", "stay",
            "اسكن", "مبيت", "ليله", "غرفه", "غرفة"
        }
        if tokens & hotel_keywords:
            return "fayoum_hotels", 1.0

        # Restaurants — أكل / جوع / كافيه
        restaurant_keywords = {
            "مطعم", "مطاعم", "اكل", "جوعان", "كافيه", "كافيهات",
            "restaurant", "restaurants", "food", "eat", "hungry", "cafe", "cafes",
            "اكلات", "مطبخ", "وجبه", "وجبة", "فطار", "غدا", "عشا",
            "breakfast", "lunch", "dinner", "meal", "عايز ياكل", "اكل حلو",
            "مطعم حلو", "اكل كويس", "اكل زين", "بيتزا", "كشري", "فول",
            "شاورما", "مشاوي", "سمك", "fish", "grill", "pizza"
        }
        if tokens & restaurant_keywords:
            return "fayoum_restaurants", 1.0

        # Tour Guides — مرشد / دليل / جولة
        tourguide_keywords = {
            "مرشد", "مرشدين", "تورجايد", "دليل", "tourguide", "guide", "guides",
            "جوله", "جولة", "tour", "tours", "يرشدني", "يدلني", "يصحبني",
            "معاي", "برنامج سياحي", "خطة رحله", "trip plan", "local guide"
        }
        if (tokens & tourguide_keywords) or "tour guide" in normalized or "مرشد سياحي" in normalized:
            return "fayoum_tourguides", 1.0

        # Attractions — أماكن / مزارات / تجوال
        attraction_keywords = {
            "معالم", "معلم", "مزار", "مزارات", "attraction", "attractions", "sightseeing",
            "أزور", "ازور", "اتفرج", "تفرج", "اتجول", "تجول", "اشوف", "شوف",
            "visit", "see", "explore", "اماكن", "مكان", "اماكن حلوه",
            "بحيره", "بحيرة", "وادي", "قصر", "هرم", "نهر", "شلال",
            "lake", "valley", "pyramid", "museum", "park", "nature", "طبيعه",
            "رحله", "رحلة", "سياحه", "سياحة", "تاريخ", "historic", "جميل",
            "وادي الريان", "بحيرة قارون", "قارون", "وادي الحيتان"
        }
        if tokens & attraction_keywords:
            return "fayoum_attractions", 1.0

        proba = self.model.predict_proba([normalized])[0]
        best_idx = proba.argmax()
        intent = self.model.classes_[best_idx]
        confidence = float(proba[best_idx])
        return intent, confidence
