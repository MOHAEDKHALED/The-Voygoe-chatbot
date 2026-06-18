"""
response_builder.py – Builds the final structured response for the frontend.
Each response has: message, type (text|card|emergency|fallback), data, intent, language.
"""

# ── Fallback messages ─────────────────────────────────────────────────────────
FALLBACK_AR = {
    "message": (
        "عذراً، مش فاهم سؤالك كويس 😅\n\n"
        "ممكن تسألني عن:\n"
        "🏨 **فنادق الفيوم** – مثال: *أحسن فندق في الفيوم*\n"
        "🏛️ **معالم سياحية** – مثال: *عايز أزور وادي الريان*\n"
        "🍔 **مطاعم وكافيهات** – مثال: *مطاعم في الفيوم*\n"
        "🧭 **مرشدين سياحيين** – مثال: *عايز مرشد سياحي*\n"
        "🚨 **طوارئ** – مثال: *محتاج إسعاف*"
    ),
    "type": "fallback",
    "data": {
        "suggestions": ["فنادق الفيوم", "معالم سياحية", "مطاعم", "مرشد سياحي", "طوارئ"]
    }
}

FALLBACK_EN = {
    "message": (
        "Sorry, I didn't quite understand that 😅\n\n"
        "You can ask me about:\n"
        "🏨 **Fayoum Hotels** – e.g. *Best hotel in Fayoum*\n"
        "🏛️ **Attractions** – e.g. *I want to visit Wadi El Rayan*\n"
        "🍔 **Restaurants** – e.g. *Best restaurant in Fayoum*\n"
        "🧭 **Tour Guides** – e.g. *Find a local guide*\n"
        "🚨 **Emergency** – e.g. *I need an ambulance*"
    ),
    "type": "fallback",
    "data": {
        "suggestions": ["Fayoum Hotels", "Attractions", "Restaurants", "Tour Guides", "Emergency"]
    }
}

# ── Hotels ────────────────────────────────────────────────────────────────────
HOTELS_RESPONSE_AR = {
    "message": (
        "🏨 **فنادق الفيوم**\n\n"
        "إليك أفضل خيارات الإقامة في الفيوم.\n"
        "اضغط على أي فندق لرؤية التفاصيل والحجز المباشر."
    ),
    "type": "card",
}

HOTELS_RESPONSE_EN = {
    "message": (
        "🏨 **Fayoum Hotels**\n\n"
        "Here are the best accommodation options in Fayoum.\n"
        "Tap any hotel to see details and book directly."
    ),
    "type": "card",
}

# ── Attractions ───────────────────────────────────────────────────────────────
ATTRACTIONS_RESPONSE_AR = {
    "message": (
        "🏛️ **المعالم السياحية بالفيوم**\n\n"
        "الفيوم مليانة أماكن رائعة! إليك أبرز المعالم:"
    ),
    "type": "card",
}

ATTRACTIONS_RESPONSE_EN = {
    "message": (
        "🏛️ **Fayoum Attractions**\n\n"
        "Fayoum is full of amazing places! Here are the top attractions:"
    ),
    "type": "card",
}

# ── Restaurants ───────────────────────────────────────────────────────────────
RESTAURANTS_RESPONSE_AR = {
    "message": (
        "🍔 **مطاعم الفيوم**\n\n"
        "إليك أفضل المطاعم وأماكن تناول الطعام في الفيوم.\n"
        "اضغط على أي مطعم لرؤية التفاصيل والموقع."
    ),
    "type": "card",
}

RESTAURANTS_RESPONSE_EN = {
    "message": (
        "🍔 **Fayoum Restaurants**\n\n"
        "Here are the best dining options and restaurants in Fayoum.\n"
        "Tap any restaurant to see details and locations."
    ),
    "type": "card",
}

# ── Tour Guides ───────────────────────────────────────────────────────────────
TOURGUIDES_RESPONSE_AR = {
    "message": (
        "🧭 **المرشدين السياحيين بالفيوم**\n\n"
        "إليك المرشدين السياحيين المعتمدين لمساعدتك في رحلتك.\n"
        "اضغط على أي مرشد للتواصل معه مباشرة."
    ),
    "type": "card",
}

TOURGUIDES_RESPONSE_EN = {
    "message": (
        "🧭 **Fayoum Tour Guides**\n\n"
        "Here are certified local tour guides to help you explore Fayoum.\n"
        "Tap any guide to contact them directly."
    ),
    "type": "card",
}


def build_hotels_response(lang: str, hotels_data: list) -> dict:
    base = HOTELS_RESPONSE_AR if lang == "ar" else HOTELS_RESPONSE_EN
    return {
        **base,
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
                    "link": f"http://voyagoo.runasp.net/hotels/{h.get('id')}"
                }
                for h in (hotels_data or [])
            ]
        }
    }


def build_attractions_response(lang: str, attractions_data: list) -> dict:
    base = ATTRACTIONS_RESPONSE_AR if lang == "ar" else ATTRACTIONS_RESPONSE_EN
    return {
        **base,
        "intent": "fayoum_attractions",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": a.get("id"),
                    "name": a.get("name") or a.get("nameAr") or "—",
                    "image": a.get("imageUrl") or a.get("image"),
                    "description": a.get("description") or a.get("descriptionAr"),
                    "link": f"http://voyagoo.runasp.net/Attractions/{a.get('id')}"
                }
                for a in (attractions_data or [])
            ]
        }
    }


def build_restaurants_response(lang: str, restaurants_data: list) -> dict:
    base = RESTAURANTS_RESPONSE_AR if lang == "ar" else RESTAURANTS_RESPONSE_EN
    return {
        **base,
        "intent": "fayoum_restaurants",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": r.get("id"),
                    "name": r.get("name") or r.get("nameAr") or "—",
                    "image": r.get("imageUrl") or r.get("image"),
                    "rating": r.get("rating"),
                    "link": f"http://voyagoo.runasp.net/Restaurants/{r.get('id')}"
                }
                for r in (restaurants_data or [])
            ]
        }
    }


def build_tourguides_response(lang: str, tourguides_data: list) -> dict:
    base = TOURGUIDES_RESPONSE_AR if lang == "ar" else TOURGUIDES_RESPONSE_EN
    return {
        **base,
        "intent": "fayoum_tourguides",
        "language": lang,
        "data": {
            "items": [
                {
                    "id": tg.get("id"),
                    "name": tg.get("name") or tg.get("nameAr") or "—",
                    "image": tg.get("imageUrl") or tg.get("image"),
                    "rating": tg.get("rating"),
                    "link": f"http://voyagoo.runasp.net/TourGuides/{tg.get('id')}"
                }
                for tg in (tourguides_data or [])
            ]
        }
    }


def build_fallback(lang: str) -> dict:
    base = FALLBACK_AR if lang == "ar" else FALLBACK_EN
    return {**base, "intent": "unknown", "language": lang}

