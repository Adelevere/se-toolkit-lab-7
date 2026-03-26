"""Telegram bot entry point with --test mode."""

import argparse
import asyncio
import sys

from config import settings
from handlers.commands import (
    handle_start,
    handle_help,
    handle_health,
    handle_labs,
    handle_scores,
)
from services.lms_client import LMSClient


async def process_command(command: str, lms_client: LMSClient) -> str:
    """Process a command and return the response."""
    parts = command.strip().split()
    cmd = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []

    if cmd == "/start":
        return await handle_start()
    elif cmd == "/help":
        return await handle_help()
    elif cmd == "/health":
        return await handle_health(lms_client)
    elif cmd == "/labs":
        return await handle_labs(lms_client)
    elif cmd == "/scores":
        lab_name = " ".join(args) if args else ""
        return await handle_scores(lms_client, lab_name)
    else:
        return f"❓ Неизвестная команда: {cmd}\nИспользуйте /help для списка команд"


def run_test_mode(command: str) -> None:
    """Run a command in test mode and print the result."""
    lms_client = LMSClient()

    async def run() -> None:
        try:
            response = await process_command(command, lms_client)
            print(response)
        finally:
            await lms_client.close()

    asyncio.run(run())


async def run_bot() -> None:
    """Run the Telegram bot."""
    from aiogram import Bot, Dispatcher, types
    from aiogram.filters import Command

    if not settings.bot_token:
        print("❌ BOT_TOKEN is required. Set it in .env.bot.secret")
        sys.exit(1)

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message) -> None:
        lms_client = LMSClient()
        try:
            response = await handle_start()
            await message.answer(response)
        finally:
            await lms_client.close()

    @dp.message(Command("help"))
    async def cmd_help(message: types.Message) -> None:
        response = await handle_help()
        await message.answer(response)

    @dp.message(Command("health"))
    async def cmd_health(message: types.Message) -> None:
        lms_client = LMSClient()
        try:
            response = await handle_health(lms_client)
            await message.answer(response)
        finally:
            await lms_client.close()

    @dp.message(Command("labs"))
    async def cmd_labs(message: types.Message) -> None:
        lms_client = LMSClient()
        try:
            response = await handle_labs(lms_client)
            await message.answer(response)
        finally:
            await lms_client.close()

    @dp.message(Command("scores"))
    async def cmd_scores(message: types.Message) -> None:
        lms_client = LMSClient()
        try:
            lab_name = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
            response = await handle_scores(lms_client, lab_name)
            await message.answer(response)
        finally:
            await lms_client.close()

    print("🤖 Bot started...")
    await dp.start_polling(bot)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="LMS Telegram Bot")
    parser.add_argument(
        "--test",
        type=str,
        metavar="COMMAND",
        help="Run a command in test mode (e.g., --test '/start')",
    )

    args = parser.parse_args()

    if args.test:
        run_test_mode(args.test)
    else:
        asyncio.run(run_bot())


if __name__ == "__main__":
    main()
