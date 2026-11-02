# 🎣 HookLab

**Scroll-stopping hooklines for social media teams and news portals.**

HookLab is a simple web app that uses AI (Claude) to write the first line people see, the line that decides whether they stop or keep scrolling.

## Features

| Mode | You give | You get |
|---|---|---|
| 🔥 **Viral Hooks** | A topic | Viral hooklines + short on-screen visual text, each tagged with its hook style |
| 📰 **News Headlines** | A news topic or full story | Scroll-stopping headlines that stay faithful to the facts, + photo-card text |

- Platforms: Facebook, Instagram, TikTok/Reels/Shorts, LinkedIn, X, YouTube
- Languages: English, Bangla (বাংলা), Banglish
- One-click copy for every hook, and CSV download for the whole batch
- Optional team password so only your team can use the hosted app

## Who it's for

Social media managers at agencies, and editorial teams at news portals.

## Quick start (run on your computer)

```bash
git clone https://github.com/<your-username>/hooklab.git
cd hooklab
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then add your API key
streamlit run app.py
```

The app opens at http://localhost:8501.

## Deploy free on Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, click **Create app**.
3. Pick this repo, branch `main`, main file `app.py`.
4. Under **Advanced settings → Secrets**, paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   APP_PASSWORD = "your-team-password"
   ```
5. Click **Deploy**. Share the link with your team.

## Configuration

| Setting | Required | What it does |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Your key from [console.anthropic.com](https://console.anthropic.com) |
| `APP_PASSWORD` | No | Team password screen before the app opens |
| `HOOKLAB_MODEL` | No | Claude model to use (default `claude-sonnet-5-5`) |

## Project structure

```
hooklab/
├── app.py                  # Streamlit web interface
├── hooklab/
│   ├── prompts.py          # Prompt templates for each mode
│   └── generator.py        # Calls Claude and parses the hooks
├── requirements.txt
└── .streamlit/
    ├── config.toml         # Theme
    └── secrets.toml.example
```

**Adding a new mode** later: add a system prompt + user prompt function in `prompts.py`, a method in `generator.py`, and a new tab in `app.py`.

## Roadmap ideas

- Caption + hashtag generator
- Thumbnail text A/B variants
- Saved brand voice per client
- History of past generations

## License

MIT, see [LICENSE](LICENSE).
