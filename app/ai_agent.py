"""
ai_agent.py — Gemini AI Agent for Voyago Chatbot
Uses google-genai (new SDK) for intelligent, contextual responses.
"""

from google import genai
from google.genai import types
import asyncio
import logging
from app.config import settings

logger = logging.getLogger("voyago_ai")

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        _client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _client


# ── System Prompts ────────────────────────────────────────────────────────────

SYSTEM_AR = """أنت Voyago AI، مساعد سياحي ذكي ومتخصص في الفيوم - مصر.
أنت مثل ChatGPT بس متخصص في السياحة في الفيوم. بتفهم أسئلة المستخدمين وبتجاوب بذكاء وتفصيل.

قواعد صارمة:
1. أجب بنفس لغة المستخدم (عربي لو السؤال عربي، إنجليزي لو إنجليزي)
2. استخدم البيانات الحقيقية المعطاة لك فقط - لا تخترع أي معلومات
3. لو سألك كم عدد (مطاعم؟ فنادق؟) → احسب من البيانات وقول الرقم الحقيقي بالضبط
4. لو سألك كيف يحجز → اشرح الخطوات بالتفصيل خطوة خطوة مع الرابط المباشر
5. لو سألك يقارن → قارن بالتفصيل بناءً على التقييمات والأسعار الحقيقية
6. لو سألك عن مكان معين → ركز عليه تحديداً من البيانات
7. لو المعلومة مش موجودة في البيانات → قول "مش متاحة المعلومة دي دلوقتي" بصدق
8. ابدأ بالإجابة المباشرة - مش ترحيب طويل
9. استخدم الإيموجي في مكانها المناسب فقط
10. كن طبيعي ومحادثة - مش قوائم جافة

نبرتك: ذكي، ودود، مباشر، متحمس للفيوم كمكان سياحي رائع"""

SYSTEM_EN = """You are Voyago AI, an intelligent tourism assistant specialized in Fayoum, Egypt.
You're like ChatGPT but specialized in Fayoum tourism. You understand questions deeply and give smart, detailed answers.

Strict rules:
1. Always respond in the same language as the user
2. Use ONLY the real data provided - never invent any information
3. If asked about counts (how many restaurants? hotels?) → count from data and give exact real number
4. If asked how to book → explain step-by-step with direct link
5. If asked to compare → compare in detail based on real ratings and prices
6. If asked about a specific place → focus on it specifically from the data
7. If information is missing → honestly say "That information isn't available right now"
8. Start with the direct answer - no long greetings
9. Use emojis appropriately and sparingly
10. Be conversational and natural - not dry bullet lists

Tone: intelligent, friendly, direct, enthusiastic about Fayoum as an amazing destination"""


# ── Main AI function ──────────────────────────────────────────────────────────

async def generate_ai_response(
    user_message: str,
    lang: str,
    intent: str,
    data: dict,
) -> str:
    """
    Uses Gemini 2.0 Flash to generate an intelligent contextual response.
    Returns None if Gemini is unavailable → pipeline falls back to template.
    """
    try:
        client = _get_client()
        data_context = _build_data_context(intent, data, lang)
        system = SYSTEM_AR if lang == "ar" else SYSTEM_EN

        prompt = f"""{system}

═══ البيانات الحقيقية المتاحة ═══
{data_context}

═══ سؤال المستخدم ═══
{user_message}

تعليمات: أجب بشكل ذكي وطبيعي بناءً على البيانات الحقيقية فقط. لا تذكر كل البيانات، ركز على ما يخص السؤال تحديداً."""

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=600,
                )
            )
        )
        return response.text.strip()

    except ValueError as e:
        logger.warning(f"[AI Agent] Not configured: {e}")
        return None
    except Exception as e:
        logger.error(f"[AI Agent] Error: {e}")
        return None


def _build_data_context(intent: str, data: dict, lang: str) -> str:
    """Convert fetched API data into a readable context for Gemini."""
    if not data or not data.get("items"):
        return "لا توجد بيانات / No data available"

    items = data["items"]
    count = len(items)

    labels = {
        "ar": {
            "fayoum_hotels": f"الفنادق المتاحة — إجمالي {count} فندق:",
            "fayoum_restaurants": f"المطاعم المتاحة — إجمالي {count} مطعم:",
            "fayoum_attractions": f"المعالم السياحية — إجمالي {count} مكان:",
            "fayoum_tourguides": f"المرشدين السياحيين — إجمالي {count} مرشد:",
        },
        "en": {
            "fayoum_hotels": f"Available Hotels — total {count} hotels:",
            "fayoum_restaurants": f"Available Restaurants — total {count} restaurants:",
            "fayoum_attractions": f"Available Attractions — total {count} places:",
            "fayoum_tourguides": f"Available Tour Guides — total {count} guides:",
        }
    }

    header = labels.get(lang, labels["en"]).get(intent, f"Data ({count} items):")
    lines = [header, ""]

    for i, item in enumerate(items, 1):
        parts = [f"{i}. {item.get('name') or '—'}"]
        if item.get("rating"):   parts.append(f"⭐{item['rating']}/5")
        if item.get("price"):    parts.append(f"💰{item['price']}")
        if item.get("location"): parts.append(f"📍{item['location']}")
        if item.get("phone"):    parts.append(f"📞{item['phone']}")
        if item.get("link"):     parts.append(f"🔗{item['link']}")
        lines.append(" | ".join(parts))
        if item.get("description"):
            lines.append(f"   ↳ {item['description'][:130]}")

    return "\n".join(lines)
