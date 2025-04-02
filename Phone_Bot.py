import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.parse

# -------------------- Logging --------------------
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------- TruePeopleSearch Lookup --------------------
def lookup_number_truepeoplesearch(phone_number):
    url = f"https://www.truepeoplesearch.com/resultphone?phoneno={phone_number}"

    options = Options()
    options.headless = True  # Run Chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    try:
        if "captcha" in driver.page_source.lower() or "access denied" in driver.page_source:
            return {"captcha": True, "url": url}

        name_element = driver.find_element(By.CSS_SELECTOR, ".card-summary .h4")
        name = name_element.text.strip()

        location_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Lives in')]//following-sibling::span")
        location = location_element.text.strip() if location_element else "Location not found"

        related_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Related to')]//following-sibling::span")
        related = related_element.text.strip() if related_element else "No related information found"

        info = {"Name": name, "Location": location, "Related to": related}
    except Exception as e:
        logger.error(f"Error fetching TruePeopleSearch: {e}")
        info = {"error": f"Error fetching data: {e}", "url": url}

    driver.quit()
    return info

# -------------------- FastPeopleSearch Lookup --------------------
def lookup_number_fastpeoplesearch(phone_number):
    formatted_number = f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
    url = f"https://www.fastpeoplesearch.com/{formatted_number}"

    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)

    try:
        name_element = driver.find_element(By.CSS_SELECTOR, "h2.card-title a span.larger")
        name = name_element.text.strip()

        location_element = driver.find_element(By.CSS_SELECTOR, "h2.card-title span.grey")
        location = location_element.text.strip()

        age = "Not found"
        try:
            age_element = driver.find_element(By.XPATH, "//h3[contains(text(), 'Age:')]/following-sibling::text()")
            age = age_element.strip()
        except:
            pass

        try:
            address_element = driver.find_element(By.XPATH, "//strong/a[contains(@href, 'address')]")
            address = address_element.text.strip()
        except:
            address = "Address not found"

        info = {"Name": name, "Location": location, "Age": age, "Address": address}
    except Exception as e:
        logger.error(f"Error fetching FastPeopleSearch: {e}")
        info = {"error": f"Error fetching data: {e}", "url": url}

    driver.quit()
    return info

# -------------------- FreePeopleSearchTool URL Builder --------------------
def build_freepeoplesearch_url(phone_number):
    formatted = f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    query = f"https://freepeoplesearchtool.com/anywho#gsc.tab=0&gsc.q={urllib.parse.quote(formatted)}&gsc.sort="
    return query

# -------------------- Telegram Command Handlers --------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me a phone number, and I’ll check its details.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        phone_number = ''.join(filter(str.isdigit, update.message.text.strip()))

        if len(phone_number) == 10:
            await update.message.reply_text(f"🔍 Searching for: {phone_number}...")

            true_results = lookup_number_truepeoplesearch(phone_number)
            fast_results = lookup_number_fastpeoplesearch(phone_number)
            free_url = build_freepeoplesearch_url(phone_number)

            # --- TruePeopleSearch Section ---
            response = "🧠 TruePeopleSearch:\n"
            if true_results.get("captcha"):
                response += f"🔐 Blocked by Captcha. [Click here to view results]({true_results['url']})\n"
            elif "error" in true_results:
                response += f"⚠️ {true_results['error']}\n🔗 [Try manually]({true_results['url']})\n"
            else:
                response += (
                    f"👤 Name: {true_results.get('Name', 'N/A')}\n"
                    f"📍 Location: {true_results.get('Location', 'N/A')}\n"
                    f"👥 Related: {true_results.get('Related to', 'N/A')}\n"
                    f"🔗 [View on TruePeopleSearch](https://www.truepeoplesearch.com/resultphone?phoneno={phone_number})\n"
                )

            # --- FastPeopleSearch Section ---
            response += "\n🔎 FastPeopleSearch:\n"
            if "error" in fast_results:
                response += f"⚠️ {fast_results['error']}\n🔗 [Try manually]({fast_results['url']})\n"
            else:
                response += (
                    f"👤 Name: {fast_results.get('Name', 'N/A')}\n"
                    f"📍 Location: {fast_results.get('Location', 'N/A')}\n"
                    f"🎂 Age: {fast_results.get('Age', 'N/A')}\n"
                    f"🏠 Address: {fast_results.get('Address', 'N/A')}\n"
                    f"🔗 [View on FastPeopleSearch](https://www.fastpeoplesearch.com/{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]})\n"
                )

            # --- FreePeopleSearchTool Section ---
            response += f"\n🧰 FreePeopleSearchTool:\n[Click here to view results]({free_url})"

            await update.message.reply_text(response, parse_mode="Markdown")
        else:
            await update.message.reply_text("Please enter a valid 10-digit U.S. phone number.")
    else:
        await update.message.reply_text("Please send a phone number only.")

# -------------------- Error Handler --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling update:", exc_info=context.error)

# -------------------- Main Bot Runner --------------------
if __name__ == "__main__":
    TELEGRAM_API_KEY = "TELEGRAM_KEY_GOES_HERE"

    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()
