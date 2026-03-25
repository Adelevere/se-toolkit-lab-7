# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import logging
import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка переменных окружения
load_dotenv('.env.bot.secret')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение переменных
BOT_TOKEN = os.getenv('BOT_TOKEN')
LMS_API_URL = os.getenv('LMS_API_URL', 'http://localhost:42002')
LMS_API_KEY = os.getenv('LMS_API_KEY')
LLM_API_KEY = os.getenv('LLM_API_KEY')
LLM_API_BASE_URL = os.getenv('LLM_API_BASE_URL')
LLM_API_MODEL = os.getenv('LLM_API_MODEL', 'coder-model')

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для LMS.\n\n"
        "Доступные команды:\n"
        "/start - показать это сообщение\n"
        "/labs - список лабораторных работ\n"
        "/help - помощь"
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - показать помощь\n"
        "/labs - список лабораторных работ\n\n"
        "Бот использует LLM для понимания запросов на естественном языке."
    )

# Команда /labs - получение списка лабораторных работ из LMS API
async def labs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Получаю список лабораторных работ...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{LMS_API_URL}/items/",
                headers={"Authorization": f"Bearer {LMS_API_KEY}"}
            )
            response.raise_for_status()
            items = response.json()
            
            labs_list = []
            for item in items[:10]:
                labs_list.append(f"• {item['title']}")
            
            if labs_list:
                await update.message.reply_text(
                    "Лабораторные работы:\n" + "\n".join(labs_list)
                )
            else:
                await update.message.reply_text("Лабораторные работы не найдены.")
                
    except Exception as e:
        logger.error(f"Ошибка при запросе к LMS API: {e}")
        await update.message.reply_text(
            "Не удалось получить список лабораторных работ.\n"
            "Убедитесь, что backend запущен."
        )

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден в .env.bot.secret")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("labs", labs))
    
    logger.info("Бот запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
