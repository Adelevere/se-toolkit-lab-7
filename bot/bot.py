#!/usr/bin/env python3
import sys
import argparse
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config
from handlers import start, help_command, health, labs
from services import LMSAPIClient

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

lms_client = None

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await start()
    await update.message.reply_text(response)

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await help_command()
    await update.message.reply_text(response)

async def health_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lms_client
    response = await health(lms_client)
    await update.message.reply_text(response)

async def labs_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lms_client
    response = await labs(lms_client)
    await update.message.reply_text(response)

def test_mode(command: str):
    async def run_test():
        global lms_client
        lms_client = LMSAPIClient(Config.LMS_API_URL, Config.LMS_API_KEY)
        
        if command == "/start":
            response = await start()
        elif command == "/help":
            response = await help_command()
        elif command == "/health":
            response = await health(lms_client)
        elif command == "/labs":
            response = await labs(lms_client)
        else:
            response = f"Unknown command: {command}"
        
        print(response)
        return 0
    
    try:
        return asyncio.run(run_test())
    except Exception as e:
        logger.error(f"Test mode error: {e}")
        print(f"Error: {e}")
        return 1

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', help='Run in test mode with command', metavar='COMMAND')
    args = parser.parse_args()
    
    if args.test:
        sys.exit(test_mode(args.test))
    
    if not Config.BOT_TOKEN:
        logger.error("BOT_TOKEN is required")
        sys.exit(1)
    
    global lms_client
    lms_client = LMSAPIClient(Config.LMS_API_URL, Config.LMS_API_KEY)
    
    app = Application.builder().token(Config.BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("health", health_handler))
    app.add_handler(CommandHandler("labs", labs_handler))
    
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
