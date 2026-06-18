"""
nlp_pipeline.py – The Core Logic (Layer 2)
Orchestrates: Emergency Path → Intent Classification → API Fetch → AI Response
"""

import asyncio
from app.emergency import detect_emergency
from app.intent_classifier import IntentClassifier
from app.context_manager import add_turn, last_intent
from app.language import detect_language
from app.response_builder import (
    build_hotels_response,
    build_attractions_response,
    build_restaurants_response,
    build_tourguides_response,
    build_fallback,
)
from app.ai_agent import generate_ai_response
import app.voyago_api as api

CONFIDENCE_THRESHOLD = 0.45  # below this → fallback


class NLPPipeline:
    """
    3-path processor:
      1. Emergency Fast Path  (keyword-based, no model)
      2. Intent Classification + AI Agent (TF-IDF + Gemini)
      3. Fallback              (smart suggestions)
    """

    def __init__(self):
        print("[NLPPipeline] Loading intent classifier …")
        self.classifier = IntentClassifier()
        print("[NLPPipeline] Ready.")

    async def process(self, message: str, session_id: str, lang_hint: str = "auto") -> dict:
        # ── Detect language ────────────────────────────────────────────────
        lang = detect_language(message, lang_hint)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PATH 1 – EMERGENCY (fast, synchronous keyword check)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        emergency = detect_emergency(message)
        if emergency:
            add_turn(session_id, message, "fayoum_emergency")
            return emergency

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PATH 2 – INTENT CLASSIFICATION + AI AGENT
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        intent, confidence = self.classifier.predict(message)

        # Context boost: if last intent was hotels and new message is short/vague
        if confidence < CONFIDENCE_THRESHOLD:
            prev = last_intent(session_id)
            if prev and prev != "unknown":
                intent = prev
                confidence = CONFIDENCE_THRESHOLD

        # ── Route by intent ────────────────────────────────────────────────
        if confidence >= CONFIDENCE_THRESHOLD:
            result = await self._route(intent, lang, session_id, message)
            add_turn(session_id, message, intent)
            return result

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # PATH 3 – FALLBACK (smart suggestions)
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        add_turn(session_id, message, "unknown")
        return build_fallback(lang)

    async def _route(self, intent: str, lang: str, session_id: str, message: str) -> dict:
        """Fetch data from Voyago API, get AI response, return structured result."""

        if intent == "fayoum_hotels":
            hotels = await api.get_hotels()
            base = build_hotels_response(lang, hotels, message)

        elif intent == "fayoum_attractions":
            attractions = await api.get_attractions()
            base = build_attractions_response(lang, attractions, message)

        elif intent == "fayoum_restaurants":
            restaurants = await api.get_restaurants()
            base = build_restaurants_response(lang, restaurants, message)

        elif intent == "fayoum_tourguides":
            tourguides = await api.get_tour_guides()
            base = build_tourguides_response(lang, tourguides, message)

        elif intent == "fayoum_emergency":
            from app.emergency import EMERGENCY_RESPONSE_AR, EMERGENCY_RESPONSE_EN
            return EMERGENCY_RESPONSE_AR if lang == "ar" else EMERGENCY_RESPONSE_EN

        else:
            return build_fallback(lang)

        # ── Try AI-powered response (Gemini) ───────────────────────────────
        ai_message = await generate_ai_response(
            user_message=message,
            lang=lang,
            intent=intent,
            data=base.get("data", {}),
        )

        # If AI responded → replace template message with AI message
        if ai_message:
            base["message"] = ai_message

        return base
