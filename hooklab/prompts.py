"""Prompt templates for each HookLab mode.

Every mode asks the model to answer with JSON only, so the app can show
results as clean cards instead of raw text.
"""

PLATFORMS = [
    "Facebook",
    "Instagram",
    "TikTok / Reels / Shorts",
    "LinkedIn",
    "X (Twitter)",
    "YouTube",
]

LANGUAGES = {
    "English": "English",
    "Bangla (বাংলা)": "Bangla, written in Bengali script",
    "Banglish": "Banglish (Bengali written with English letters, casual social-media style)",
}

VIRAL_TONES = ["Bold", "Funny", "Emotional", "Curious", "Controversial", "Inspirational", "Educational"]

NEWS_TONES = ["Breaking / Urgent", "Serious", "Curious", "Human-interest", "Explainer"]


VIRAL_SYSTEM = """You are a senior social media copywriter who writes hooks for viral posts.
A hook is the first line people see before they decide to keep scrolling or stop.

Rules:
- Each hook must make someone stop scrolling within 1 second.
- Use a mix of proven hook styles: curiosity gap, bold claim, contrarian take, number/list,
  question, mini-story, warning, relatable pain point, before/after.
- Keep each hook short (ideally under 15 words) and natural for the chosen platform.
- "visual_text" is a punchy on-screen text overlay for an image or video thumbnail:
  3 to 7 words, no hashtags.
- Do not invent fake statistics, fake quotes or fake facts.
- Never repeat the same opening words across hooks.

Respond with JSON only, no extra text, in exactly this shape:
{"hooks": [{"hook": "...", "visual_text": "...", "style": "..."}]}"""


NEWS_SYSTEM = """You are a senior digital news editor who writes scroll-stopping headlines
for news portals' social media pages.

Rules:
- Stay 100% faithful to the facts in the content provided. Never add numbers, names,
  places, quotes or claims that are not in the content.
- Make it gripping, but never misleading clickbait. The post must deliver what the headline promises.
- Lead with the most newsworthy and human angle.
- Keep each headline short (ideally under 14 words).
- "visual_text" is a short text for the news photo card: 3 to 8 words.
- "angle" names the approach in 1 to 3 words (for example: impact, human story, numbers, what's next).
- If the content is too thin to know a fact, write around it instead of guessing.

Respond with JSON only, no extra text, in exactly this shape:
{"hooks": [{"hook": "...", "visual_text": "...", "angle": "..."}]}"""


def viral_user_prompt(topic: str, platform: str, tone: str, language: str, count: int, audience: str = "") -> str:
    lines = [
        f"Topic: {topic.strip()}",
        f"Platform: {platform}",
        f"Tone: {tone}",
        f"Write in: {LANGUAGES.get(language, language)}",
    ]
    if audience.strip():
        lines.append(f"Target audience: {audience.strip()}")
    lines.append(f"Write {count} different hooks.")
    return "\n".join(lines)


def news_user_prompt(content: str, tone: str, language: str, count: int, platform: str) -> str:
    return "\n".join(
        [
            "News content:",
            '"""',
            content.strip(),
            '"""',
            f"Tone: {tone}",
            f"Platform: {platform}",
            f"Write in: {LANGUAGES.get(language, language)}",
            f"Write {count} different headlines.",
        ]
    )
