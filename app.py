"""HookLab — web app entry point.

Run locally:  streamlit run app.py
"""

import csv
import io
import os

import streamlit as st

from hooklab import __version__, prompts
from hooklab.generator import DEFAULT_MODEL, HookGenerator

st.set_page_config(page_title="HookLab", page_icon="🎣", layout="centered")


def get_setting(name: str, default: str = "") -> str:
    """Read a setting from Streamlit secrets first, then environment variables."""
    try:
        if name in st.secrets:
            return str(st.secrets[name])
    except Exception:
        pass
    return os.environ.get(name, default)


# ---------- Optional password gate (so strangers can't use up your API credit) ----------
APP_PASSWORD = get_setting("APP_PASSWORD")
if APP_PASSWORD and not st.session_state.get("unlocked"):
    st.title("🎣 HookLab")
    pw = st.text_input("Team password", type="password")
    if st.button("Enter"):
        if pw == APP_PASSWORD:
            st.session_state.unlocked = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()

# ---------- API key ----------
api_key = get_setting("ANTHROPIC_API_KEY")
model = get_setting("HOOKLAB_MODEL", DEFAULT_MODEL)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    if not api_key:
        api_key = st.text_input(
            "Anthropic API key",
            type="password",
            help="Get one at console.anthropic.com. For a shared team link, set it in the app's secrets instead.",
        )
    else:
        st.success("API key loaded")
    st.caption(f"Model: `{model}`")
    st.caption(f"HookLab v{__version__}")


def to_csv(hooks, tag_label: str) -> str:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["#", "Hook", "Visual text", tag_label])
    for i, h in enumerate(hooks, 1):
        writer.writerow([i, h.hook, h.visual_text, h.tag])
    return buf.getvalue()


def show_results(hooks, tag_label: str, file_prefix: str):
    st.markdown(f"#### ✨ {len(hooks)} results")
    for i, h in enumerate(hooks, 1):
        with st.container(border=True):
            label = f" · `{h.tag}`" if h.tag else ""
            st.markdown(f"**{i}.**{label}")
            st.code(h.hook, language=None, wrap_lines=True)  # code box = built-in copy button
            if h.visual_text:
                st.caption(f"🖼️ Visual text: **{h.visual_text}**")
    st.download_button(
        "⬇️ Download as CSV",
        data=to_csv(hooks, tag_label),
        file_name=f"{file_prefix}.csv",
        mime="text/csv",
    )


def run(fn, **kwargs):
    if not api_key:
        st.warning("Add your Anthropic API key in the sidebar first.")
        return None
    try:
        with st.spinner("Cooking up hooks..."):
            return fn(**kwargs)
    except Exception as e:  # show a friendly message instead of a crash
        st.error(f"Something went wrong: {e}")
        return None


# ---------- Page ----------
st.title("🎣 HookLab")
st.caption("Scroll-stopping hooklines for social media teams and news portals.")

tab_viral, tab_news = st.tabs(["🔥 Viral Hooks", "📰 News Headlines"])

with tab_viral:
    st.markdown("Give a topic, get viral hooklines plus on-screen visual text.")
    topic = st.text_area("Topic", placeholder="e.g. Saving money on a small salary", height=80)
    c1, c2 = st.columns(2)
    platform = c1.selectbox("Platform", prompts.PLATFORMS, key="v_platform")
    tone = c2.selectbox("Tone", prompts.VIRAL_TONES, key="v_tone")
    c3, c4 = st.columns(2)
    language = c3.selectbox("Language", list(prompts.LANGUAGES), key="v_lang")
    count = c4.slider("How many?", 3, 15, 8, key="v_count")
    audience = st.text_input("Target audience (optional)", placeholder="e.g. university students in Dhaka")

    if st.button("Generate hooks", type="primary", key="v_go"):
        if not topic.strip():
            st.warning("Please enter a topic.")
        else:
            gen = HookGenerator(api_key, model) if api_key else None
            result = run(
                gen.viral_hooks if gen else None,
                topic=topic, platform=platform, tone=tone,
                language=language, count=count, audience=audience,
            )
            if result:
                st.session_state.viral_result = result

    if st.session_state.get("viral_result"):
        show_results(st.session_state.viral_result, "Style", "hooklab-viral")

with tab_news:
    st.markdown("Paste a news topic or the full story, get scroll-stopping headlines that stay true to the facts.")
    content = st.text_area(
        "News topic or content",
        placeholder="Paste the news summary or full article here...",
        height=180,
    )
    c1, c2 = st.columns(2)
    n_tone = c1.selectbox("Tone", prompts.NEWS_TONES, key="n_tone")
    n_platform = c2.selectbox("Platform", prompts.PLATFORMS, key="n_platform")
    c3, c4 = st.columns(2)
    n_language = c3.selectbox("Language", list(prompts.LANGUAGES), key="n_lang")
    n_count = c4.slider("How many?", 3, 12, 6, key="n_count")

    if st.button("Generate headlines", type="primary", key="n_go"):
        if not content.strip():
            st.warning("Please enter the news topic or content.")
        else:
            gen = HookGenerator(api_key, model) if api_key else None
            result = run(
                gen.news_hooks if gen else None,
                content=content, tone=n_tone, language=n_language,
                count=n_count, platform=n_platform,
            )
            if result:
                st.session_state.news_result = result

    if st.session_state.get("news_result"):
        show_results(st.session_state.news_result, "Angle", "hooklab-news")
        st.caption("⚠️ Always double-check names and numbers against the original story before posting.")
