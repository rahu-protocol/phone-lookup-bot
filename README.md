📄 README.md
markdown
Copy
Edit
# 📞 Telegram Phone Lookup Bot

A Telegram bot that performs phone number lookups using:

- **TruePeopleSearch.com**
- **FastPeopleSearch.com**
- **FreePeopleSearchTool.com**

It uses `Selenium` to extract information and falls back to direct URLs if a CAPTCHA is detected.

---

## 🚀 Features

- ✅ Extracts Name, Location, Relatives, Age, and Address (when available)
- 🔐 Detects CAPTCHA and provides manual fallback links
- 🧰 Provides direct links for all three services
- ✨ Designed to be fast, silent (headless), and user-friendly

---

## 🧪 Example Output

🔍 Searching for: xxxxxxxxxx...

🧠 TruePeopleSearch: 👤 Name: John Doe 📍 Location: xxx, xx 👥 Related: Jane Doe 🔗 View on TruePeopleSearch

🔎 FastPeopleSearch: 👤 Name: John Doe 📍 Location: xxx, xx 🎂 Age: xx 🏠 Address: xxx xxxx Ave 🔗 View on FastPeopleSearch

🧰 FreePeopleSearchTool: Click here to view results

yaml
Copy
Edit

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/phone-lookup-bot.git
cd phone-lookup-bot
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Set up your bot
Edit the TELEGRAM_API_KEY at the bottom of the script with your bot’s token from BotFather.

4. Run the bot
bash
Copy
Edit
python Phone_Bot.py
🧰 Requirements
Python 3.8+

Google Chrome installed

Internet access

🔐 Disclaimer
This tool is for educational and OSINT research purposes only. Please ensure you're complying with local laws and the terms of service of the sites used.
