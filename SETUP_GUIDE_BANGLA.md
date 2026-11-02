# HookLab Setup Guide (Banglish)

Kono coding experience chhara-o ei guide follow kore tool ta online e chalu korte parbe. Mot 4 ta dhap, 20-30 minute lagbe.

---

## Dhap 1: GitHub account khola

1. **github.com** e jao → **Sign up** click koro
2. Email, password, aar ekta **username** dao (jemon `yourname` ba `yourcompany-dev`). Username pore repo link e dekhabe: `github.com/username/hooklab`
3. Email e asha code diye verify koro
4. Free plan ei thako, ar kichu lagbe na

> **Tip:** Settings → Password and authentication → **Two-factor authentication** on kore dao. Account safe thakbe.

---

## Dhap 2: Repo banano aar file upload

Git command na shikheo browser theke shob kora jay:

1. GitHub e upore dane **+** → **New repository**
2. Repository name: `hooklab`
3. **Public** ba **Private** bachai koro (company tool hole Private valo)
4. Kono box tick koro na (README, license already ache) → **Create repository**
5. Next page e **"uploading an existing file"** link e click koro
6. Zip ta extract kore `hooklab` folder er **bhetorer shob kichu** drag kore browser e chere dao
7. Niche **Commit changes** click koro

> ⚠️ **`.streamlit` folder ta khub important.** Mac/Windows e dot (.) diye shuru howa folder hidden thake.
> - Mac: Finder e `Cmd + Shift + .` chaple dekhabe
> - Windows: File Explorer → View → **Hidden items** tick koro
>
> Upload er por repo te `.streamlit/config.toml` ache kina check koro. (`secrets.toml` kokhono upload korbe na, eta `.gitignore` e already block kora.)

---

## Dhap 3: Anthropic API key neya

Tool ta hooklines banate Claude AI use kore, tai ekta API key lagbe.

1. **console.anthropic.com** e account kholo
2. **Billing** e card add kore kichu credit kino (choto amount diye shuru korle-i hobe; prottek generation e khub alpo khoroch hoy)
3. **API Keys** → **Create Key** → key ta copy kore kothao safe rakho (`sk-ant-...` diye shuru)

> ⚠️ Ei key kauke dibe na, GitHub e kokhono paste korbe na. Key leak hole onno keu tomar credit khoroch korte parbe.

---

## Dhap 4: Free te online e chalu kora (Streamlit Cloud)

1. **share.streamlit.io** e jao → **Continue with GitHub** diye login koro
2. **Create app** → **Deploy a public app from GitHub**
3. Repository: `username/hooklab`, Branch: `main`, Main file path: `app.py`
4. **App URL** e ekta shundor naam dao (jemon `hooklab-yourcompany`)
5. **Advanced settings** → **Secrets** box e ei duita line paste koro:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-tomar-key-ekhane"
   APP_PASSWORD = "team-er-jonno-ekta-password"
   ```
6. **Deploy** click koro. 2-3 minute por app chalu hobe 🎉

Ekhon link ta team ke dao, aar password ta bolo. Password chhara keu use korte parbe na, tai tomar API credit safe.

---

## Pore update korbo kivabe?

- GitHub e repo te gie je file change korbe oita khule ✏️ (pencil) icon e click kore edit koro → **Commit changes**
- Streamlit Cloud nijei 1-2 minute er moddhe notun version chalu kore dibe

Notun feature lagle (jemon caption generator, hashtag) amake bolo, ami code likhe dibo, tumi shudhu file replace korbe.

---

## Shomossha hole

| Shomossha | Shomadhan |
|---|---|
| "API key" warning dekhay | Streamlit app settings → Secrets e key thik vabe paste hoyeche kina dekho (quote soho) |
| "Something went wrong: credit balance" | console.anthropic.com e billing e credit add koro |
| App er color/theme ashe nai | `.streamlit/config.toml` upload hoy nai, Dhap 2 er hidden folder note ta dekho |
| App ghumiye ache ("app is asleep") | Free plan e onek din use na hole ghumay, "Wake up" button chaple abar chalu hoy |
