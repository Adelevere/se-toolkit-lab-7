#!/usr/bin/env python3
import sys
import argparse
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import Config
from handlers.commands import start, help_command, health, labs, scores
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

async def scores_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global lms_client
    lab_name = ' '.join(context.args) if context.args else ''
    response = await scores(lms_client, lab_name)
    await update.message.reply_text(response)

def test_mode(command: str):
    """Run bot in test mode - processes command and prints output"""
    async def run_test():
        global lms_client
        lms_client = LMSAPIClient(Config.LMS_API_URL, Config.LMS_API_KEY)
        
        parts = command.split()
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        
        if cmd == "/start":
            response = await start()
        elif cmd == "/help":
            response = await help_command()
        elif cmd == "/health":
            response = await health(lms_client)
        elif cmd == "/labs":
            response = await labs(lms_client)
        elif cmd == "/scores":
            if not arg:
                response = "❌ Please specify a lab name.\nExample: /scores lab-01"
            else:
                response = await scores(lms_client, arg)
        else:
            response = f"Unknown command: {cmd}\nTry /help for available commands."
        
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
    app.add_handler(CommandHandler("scores", scores_handler))
    
    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
