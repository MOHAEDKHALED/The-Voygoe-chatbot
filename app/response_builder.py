"""
response_builder.py – Builds personalized structured responses for the frontend.
Each response has: message, type (text|card|emergency|fallback), data, intent, language.
"""

import re


# ── Personalization helpers ───────────────────────────────────────────────────

def _norm(text: str) -> str:
    """Quick Arabic normalization for keyword matching."""
    text = text.lower().strip()
    text = re.sub(r"[أإآ]", "ا", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)
    return text


def _hotel_intro(lang: str, message: str) -> str:
    m = _norm(message)
    if lang == "ar":
        if any(w in m for w in ["رخيص", "ارخص", "بسيط", "ميزانيه", "اقتصاد"]):
            return "💰 بتدور على فندق بسعر كويس؟ إليك أفضل الخيارات المناسبة للميزانية:"
        if any(w in m for w in ["فاخر", "راقي", "لوكس", "vip", "5 نجوم", "خمس نجوم"]):
            return "👑 عايز تفخم؟ إليك أفخم الفنادق في الفيوم:"
        if any(w in m for w in ["بحيره", "بحيرة", "قارون", "ليك"]):
            return "🌊 عايز فندق قريب من البحيرة؟ إليك الأقرب لبحيرة قارون:"
        if any(w in m for w in ["هادي", "هدوء", "هدوه", "ريلاكس", "استرخاء"]):
            return "🌿 عايز تسترخي بعيد عن الضوضاء؟ إليك أهدأ الفنادق:"
        if any(w in m for w in ["عيله", "عائله", "اطفال", "أطفال", "فاميلي"]):
            return "👨‍👩‍👧 رحلة عيلة؟ إليك الفنادق الأنسب للعيلات:"
        if any(w in m for w in ["احجز", "حجز", "حجزت", "ابوك", "ليله"]):
            return "📅 تمام! إليك أفضل الفنادق المتاحة في الفيوم — اضغط لحجز مباشر:"
        return "🏨 إليك أفضل خيارات الإقامة في الفيوم — اضغط على أي فندق لرؤية التفاصيل:"
    else:
        if any(w in m for w in ["cheap", "budget", "affordable", "low cost"]):
            return "💰 Looking for budget-friendly options? Here are the best affordable hotels:"
        if any(w in m for w in ["luxury", "5 star", "vip", "fancy", "premium"]):
            return "👑 Looking for luxury? Here are Fayoum's finest hotels:"
        if any(w in m for w in ["lake", "qarun", "near water"]):
            return "🌊 Want a hotel near the lake? Here are the closest to Lake Qarun:"
        if any(w in m for w in ["quiet", "peaceful", "relax", "calm"]):
            return "🌿 Looking for peace and quiet? Here are Fayoum's most serene hotels:"
        if any(w in m for w in ["family", "kids", "children"]):
            return "👨‍👩‍👧 Family trip? Here are the most family-friendly hotels:"
        return "🏨 Here are the best accommodation options in Fayoum — tap any hotel for details:"


def _restaurant_intro(lang: str, message: str) -> str:
    m = _norm(message)
    if lang == "ar":
        if any(w in m for w in ["سمك", "اسماك", "بحري", "مأكولات بحريه"]):
            return "🐟 بتدور على سمك طازج؟ إليك أفضل مطاعم الأسماك في الفيوم:"
        if any(w in m for w in ["مشوي", "مشاوي", "كباب", "كفته", "شواء"]):
            return "🔥 عايز مشاوي؟ إليك أفضل مطاعم المشويات في الفيوم:"
        if any(w in m for w in ["بيتزا", "إيطالي", "ايطالي", "باستا"]):
            return "🍕 عايز إيطالي؟ إليك الأماكن المناسبة:"
        if any(w in m for w in ["فطار", "فطور", "صباح", "breakfast"]):
            return "☀️ محتاج فطار كويس؟ إليك أفضل الأماكن للفطار في الفيوم:"
        if any(w in m for w in ["كافيه", "كافيهات", "قهوه", "كوفي", "cafe"]):
            return "☕ عايز كافيه حلو؟ إليك أجمل الكافيهات في الفيوم:"
        if any(w in m for w in ["جوعان", "اكل", "طعام", "وجبه"]):
            return "🍽️ جعلك الله! إليك أفضل المطاعم في الفيوم دلوقتي:"
        if any(w in m for w in ["عشا", "غدا", "دنر", "dinner", "lunch"]):
            return "🌙 عايز تتعشى كويس؟ إليك أحسن خيارات العشا في الفيوم:"
        return "🍔 إليك أفضل المطاعم وأماكن الأكل في الفيوم — اضغط لرؤية التفاصيل:"
    else:
        if any(w in m for w in ["fish", "seafood", "sea food"]):
            return "🐟 Looking for fresh seafood? Here are the best fish restaurants in Fayoum:"
        if any(w in m for w in ["grill", "bbq", "kebab", "grilled"]):
            return "🔥 Craving grilled food? Here are the best grill restaurants:"
        if any(w in m for w in ["pizza", "italian", "pasta"]):
            return "🍕 Looking for Italian? Here are your options:"
        if any(w in m for w in ["breakfast", "morning", "brunch"]):
            return "☀️ Need a good breakfast? Here are the best morning spots in Fayoum:"
        if any(w in m for w in ["cafe", "coffee", "tea"]):
            return "☕ Looking for a nice café? Here are Fayoum's best cafes:"
        if any(w in m for w in ["hungry", "eat", "food", "meal"]):
            return "🍽️ Hungry? Here are the best restaurants in Fayoum right now:"
        return "🍔 Here are the best dining options in Fayoum — tap any for details:"


def _attractions_intro(lang: str, message: str) -> str:
    m = _norm(message)
    if lang == "ar":
        if any(w in m for w in ["وادي الريان", "الريان"]):
            return "🌊 وادي الريان رائع! إليك أبرز المعالم هناك وحواليه:"
        if any(w in m for w in ["وادي الحيتان", "الحيتان", "whales"]):
            return "🐋 وادي الحيتان من أروع المواقع الجيولوجية في العالم! إليك تفاصيله:"
        if any(w in m for w in ["بحيره", "بحيرة", "قارون"]):
            return "🌊 بحيرة قارون جميلة! إليك أفضل الأماكن حواليها:"
        if any(w in m for w in ["قصر", "قصور", "تاريخ", "اثري", "أثري"]):
            return "🏛️ عاشق التاريخ؟ إليك أبرز المواقع الأثرية في الفيوم:"
        if any(w in m for w in ["طبيعه", "طبيعة", "خضرا", "خضراء", "nature"]):
            return "🌿 عايز تتنفس هواء نظيف؟ إليك أجمل المناطق الطبيعية في الفيوم:"
        if any(w in m for w in ["عيله", "عائله", "اطفال", "أطفال"]):
            return "👨‍👩‍👧 رحلة عيلة؟ إليك الأماكن الأنسب للعيلات والأطفال:"
        if any(w in m for w in ["تصوير", "فوتو", "كاميرا", "صور"]):
            return "📸 عاشق التصوير؟ إليك أجمل الأماكن للتصوير في الفيوم:"
        return "🏛️ الفيوم مليانة أماكن رائعة! إليك أبرز المعالم السياحية:"
    else:
        if any(w in m for w in ["wadi el rayan", "rayan"]):
            return "🌊 Wadi El Rayan is stunning! Here are the highlights:"
        if any(w in m for w in ["whale", "wadi el hitan"]):
            return "🐋 Wadi El Hitan is a UNESCO World Heritage Site! Here are the details:"
        if any(w in m for w in ["lake", "qarun"]):
            return "🌊 Lake Qarun is beautiful! Here are the best spots around it:"
        if any(w in m for w in ["history", "ancient", "pharaoh", "historic"]):
            return "🏛️ History lover? Here are Fayoum's best historical sites:"
        if any(w in m for w in ["nature", "green", "outdoor"]):
            return "🌿 Looking for nature? Here are Fayoum's most beautiful natural spots:"
        return "🏛️ Fayoum is full of amazing places! Here are the top attractions:"


def _tourguide_intro(lang: str, message: str) -> str:
    m = _norm(message)
    if lang == "ar":
        if any(w in m for w in ["يوم كامل", "يوم تامن", "فل داي", "full day"]):
            return "🧭 عايز مرشد ليوم كامل؟ إليك المرشدين المتاحين لجولات كاملة:"
        if any(w in m for w in ["انجليزي", "إنجليزي", "english", "foreign"]):
            return "🗣️ عايز مرشد بيتكلم إنجليزي؟ إليك المرشدين المعتمدين:"
        if any(w in m for w in ["رخيص", "تمن", "سعر", "اسعار"]):
            return "💰 عايز مرشد بسعر معقول؟ إليك الخيارات المتاحة:"
        if any(w in m for w in ["شاطر", "محترف", "خبره", "خبير"]):
            return "⭐ عايز مرشد محترف وعنده خبرة؟ إليك المرشدين الأعلى تقييماً:"
        return "🧭 إليك المرشدين السياحيين المعتمدين في الفيوم — اضغط للتواصل مباشرة:"
    else:
        if any(w in m for w in ["full day", "whole day", "all day"]):
            return "🧭 Need a full-day guide? Here are guides available for full tours:"
        if any(w in m for w in ["english", "arabic", "language"]):
            return "🗣️ Here are certified guides who speak your language:"
        if any(w in m for w in ["cheap", "affordable", "price", "cost"]):
            return "💰 Looking for an affordable guide? Here are your options:"
        return "🧭 Here are certified local tour guides — tap to contact them directly:"


# ── Fallback ──────────────────────────────────────────────────────────────────

FALLBACK_AR = {
    "message": (
        "معلش، مش فاهم سؤالك كويس 😅\n\n"
        "ممكن تسألني عن:\n"
        "🏨 **فنادق الفيوم** — مثال: *عايز أحجز فندق*\n"
        "🏛️ **معالم سياحية** — مثال: *عايز أتجول في الفيوم*\n"
        "🍔 **مطاعم وكافيهات** — مثال: *أنا جوعان عايز آكل*\n"
        "🧭 **مرشدين سياحيين** — مثال: *عايز حد يرشدني*\n"
        "🚨 **طوارئ** — مثال: *محتاج إسعاف*"
    ),
    "type": "fallback",
    "data": {
        "suggestions": ["فنادق الفيوم", "أماكن سياحية", "مطاعم", "مرشد سياحي", "طوارئ"]
    }
}

FALLBACK_EN = {
    "message": (
        "Sorry, I didn't quite understand that 😅\n\n"
        "You can ask me about:\n"
        "🏨 **Fayoum Hotels** — e.g. *I want to book a hotel*\n"
        "🏛️ **Attractions** — e.g. *Best places to visit in Fayoum*\n"
        "🍔 **Restaurants** — e.g. *I'm hungry, where to eat?*\n"
        "🧭 **Tour Guides** — e.g. *I need a local guide*\n"
        "🚨 **Emergency** — e.g. *I need an ambulance*"
    ),
    "type": "fallback",
    "data": {
        "suggestions": ["Fayoum Hotels", "Attractions", "Restaurants", "Tour Guides", "Emergency"]
    }
}


# ── Response builders ─────────────────────────────────────────────────────────

def build_hotels_response(lang: str, hotels_data: list, message: str = "") -> dict:
    intro = _hotel_intro(lang, message)
    return {
        "message": intro,
        "type": "card",
        "intent": "fayoum_hotels",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": h.get("id"),
                    "name": h.get("name") or h.get("nameAr") or "—",
                    "image": h.get("imageUrl") or h.get("image"),
                    "rating": h.get("rating"),
                    "price": h.get("pricePerNight") or h.get("price"),
                    "description": h.get("description") or h.get("descriptionAr"),
                    "location": h.get("location") or h.get("address"),
                    "phone": h.get("phone") or h.get("phoneNumber"),
                    "link": f"http://voyagoo.runasp.net/hotels/{h.get('id')}"
                }
                for h in (hotels_data or [])
            ]
        }
    }


def build_attractions_response(lang: str, attractions_data: list, message: str = "") -> dict:
    intro = _attractions_intro(lang, message)
    return {
        "message": intro,
        "type": "card",
        "intent": "fayoum_attractions",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": a.get("id"),
                    "name": a.get("name") or a.get("nameAr") or "—",
                    "image": a.get("imageUrl") or a.get("image"),
                    "description": a.get("description") or a.get("descriptionAr"),
                    "location": a.get("location") or a.get("address"),
                    "category": a.get("category"),
                    "link": f"http://voyagoo.runasp.net/Attractions/{a.get('id')}"
                }
                for a in (attractions_data or [])
            ]
        }
    }


def build_restaurants_response(lang: str, restaurants_data: list, message: str = "") -> dict:
    intro = _restaurant_intro(lang, message)
    return {
        "message": intro,
        "type": "card",
        "intent": "fayoum_restaurants",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": r.get("id"),
                    "name": r.get("name") or r.get("nameAr") or "—",
                    "image": r.get("imageUrl") or r.get("image"),
                    "rating": r.get("rating"),
                    "description": r.get("description") or r.get("descriptionAr"),
                    "location": r.get("location") or r.get("address"),
                    "phone": r.get("phone") or r.get("phoneNumber"),
                    "link": f"http://voyagoo.runasp.net/Restaurants/{r.get('id')}"
                }
                for r in (restaurants_data or [])
            ]
        }
    }


def build_tourguides_response(lang: str, tourguides_data: list, message: str = "") -> dict:
    intro = _tourguide_intro(lang, message)
    return {
        "message": intro,
        "type": "card",
        "intent": "fayoum_tourguides",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": tg.get("id"),
                    "name": tg.get("name") or tg.get("nameAr") or "—",
                    "image": tg.get("imageUrl") or tg.get("image"),
                    "rating": tg.get("rating"),
                    "description": tg.get("description") or tg.get("descriptionAr"),
                    "phone": tg.get("phone") or tg.get("phoneNumber"),
                    "languages": tg.get("languages"),
                    "link": f"http://voyagoo.runasp.net/TourGuides/{tg.get('id')}"
                }
                for tg in (tourguides_data or [])
            ]
        }
    }


def build_fallback(lang: str) -> dict:
    base = FALLBACK_AR if lang == "ar" else FALLBACK_EN
    return {**base, "intent": "unknown", "language": lang}
