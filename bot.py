# Add these imports at the top if not present
from telegram.ext import Application, JobQueue
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from datetime import datetime
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackContext, CallbackQueryHandler
import requests
import json
import time
import threading
import re
import urllib.parse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID_STR = os.getenv("AUTHORIZED_USER_ID")
FSHARE_USERNAME = os.getenv("FSHARE_USERNAME")
FSHARE_PASSWORD = os.getenv("FSHARE_PASSWORD")
API_KEY = os.getenv("API_KEY")
ARIA2_RPC_URL = os.getenv("ARIA2_RPC_URL", "http://localhost:6800/jsonrpc") # Default if not set
ARIA2_SECRET = os.getenv("ARIA2_SECRET")
SAVE_DIR = os.getenv("SAVE_DIR", "D:/Getlink") # Default if not set
CUSTOM_STORAGE_URL = os.getenv("CUSTOM_STORAGE_URL") # Optional

# Validate required environment variables
if not BOT_TOKEN:
    raise ValueError("Missing required environment variable: BOT_TOKEN")
if not AUTHORIZED_USER_ID_STR:
    raise ValueError("Missing required environment variable: AUTHORIZED_USER_ID")
if not FSHARE_USERNAME:
    raise ValueError("Missing required environment variable: FSHARE_USERNAME")
if not FSHARE_PASSWORD:
    raise ValueError("Missing required environment variable: FSHARE_PASSWORD")
if not API_KEY:
    raise ValueError("Missing required environment variable: API_KEY")

try:
    AUTHORIZED_USER_ID = int(AUTHORIZED_USER_ID_STR)
except ValueError:
    raise ValueError("AUTHORIZED_USER_ID must be an integer")

active_downloads = {}

# Restrict bot usage
def restricted(func):
    def wrapper(update: Update, context: CallbackContext):
        user_id = update.effective_user.id
        if user_id != AUTHORIZED_USER_ID:
            update.message.reply_text("🚫 You are not authorized to use this bot.")
            logging.warning(f"Unauthorized access attempt from user ID: {user_id}")
            return
        return func(update, context)
    return wrapper

# Fshare Login
def fshare_login():
    logging.info("Logging into Fshare...")
    login_url = "https://api.fshare.vn/api/user/login"
    login_data = {"user_email": FSHARE_USERNAME, "password": FSHARE_PASSWORD, "app_key": API_KEY}
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "TESTGFS-M6ULNU"
    }
    
    response = requests.post(login_url, json=login_data, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data.get("code") == 200:
            logging.info("✅ Fshare login successful!")
            return data.get("token"), data.get("session_id")
    
    logging.error("❌ Fshare login failed!")
    return None, None

# Get Fshare Direct Link
def get_fshare_link(url):
    logging.info(f"Fetching Fshare download link for: {url}")
    
    # Extract file ID from URL
    match = re.search(r'/file/([A-Za-z0-9]+)', url)
    if not match:
        logging.error("❌ Invalid Fshare URL!")
        return None, None, "❌ Invalid Fshare URL!"
    
    file_id = match.group(1)
    logging.info(f"Extracted file ID: {file_id}")
    
    token, session_id = fshare_login()
    
    if not token or not session_id:
        return None, None, "❌ Login failed!"
    
    headers = {
        "Cookie": f"session_id={session_id}",
        "User-Agent": "TESTGFS-M6ULNU"
    }
    download_data = {"token": token, "url": f"https://www.fshare.vn/file/{file_id}", "password": "", "zipflag": 0}
    response = requests.post("https://api.fshare.vn/api/session/download", json=download_data, headers=headers)
    
    logging.info(f"Response status code: {response.status_code}")
    logging.info(f"Response content: {response.content}")
    
    if response.status_code == 200:
        result = response.json()
        location = result.get("location")
        if location:
            filename = urllib.parse.unquote(location.split('/')[-1]).replace(' ', '_')
            logging.info(f"✅ Fetched direct link: {location}")
            logging.info(f"Extracted filename: {filename}")
            return location, filename, None
    
    logging.error("❌ Failed to fetch download link from Fshare!")
    return None, None, "❌ Failed to get download link!"

# Handle All Links
@restricted
async def download_link(update: Update, context: CallbackContext):
    message = update.message.text
    user_id = update.effective_user.id
    logging.info(f"📥 Received message from {user_id}: {message}")

    direct_link, filename, error = get_fshare_link(message)
    if error:
        await update.message.reply_text(error)
        logging.error(f"❌ Error: {error}")
    else:
        await update.message.reply_text(f"🔗 **Direct link:** `{direct_link}`", parse_mode="Markdown")
        logging.info(f"✅ Direct link sent: {direct_link}")

def main():
    try:
        logging.info("🤖 Telegram bot is starting...")

        # Initialize scheduler first with proper timezone
        scheduler = AsyncIOScheduler(timezone="UTC")  # Explicitly use "UTC" timezone string
        
        # Create application 
        application = (
            Application.builder()
            .token(BOT_TOKEN)
            .build()
        )

        # Configure job queue
        application.job_queue.scheduler = scheduler
        scheduler.start()

        # Add handlers
        application.add_handler(MessageHandler(None, download_link))
        
        # Start polling
        application.run_polling()

    except Exception as e:
        logging.error(f"Bot error: {e}")
        raise
    finally:
        if 'scheduler' in locals():
            scheduler.shutdown()
        logging.info("Bot stopped")

if __name__ == "__main__":
    main()
