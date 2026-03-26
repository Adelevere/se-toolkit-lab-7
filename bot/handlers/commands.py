"""Slash command handlers."""

from services.lms_client import LMSClient


async def handle_start() -> str:
    """Handle /start command."""
    return "👋 Добро пожаловать в LMS Bot!\n\nДоступные команды:\n/help — показать справку\n/health — проверить статус системы\n/labs — список лабораторных\n/scores — результаты студентов"


async def handle_help() -> str:
    """Handle /help command."""
    return """📚 Доступные команды:

/start — приветственное сообщение
/help — эта справка
/health — статус backend системы
/labs — список доступных лабораторных работ
/scores <lab> — результаты по лабораторной

Вы также можете задавать вопросы естественным языком, например:
• "Какие есть лабораторные?"
• "Какая лабораторная самая сложная?"
• "Покажи результаты по lab-1"
"""


async def handle_health(lms_client: LMSClient) -> str:
    """Handle /health command."""
    try:
        status = await lms_client.get_health()
        if status.get("status") == "healthy":
            return "✅ Система работает нормально"
        return f"⚠️ Статус: {status}"
    except Exception as e:
        return f"❌ Ошибка подключения к backend: {e}"


async def handle_labs(lms_client: LMSClient) -> str:
    """Handle /labs command."""
    try:
        labs = await lms_client.get_items()
        if not labs:
            return "📭 Лабораторные работы не найдены"
        
        result = "📚 Доступные лабораторные:\n\n"
        for lab in labs:
            name = lab.get("name", "Без названия")
            description = lab.get("description", "")[:100]
            result += f"• {name}\n  {description}\n\n"
        return result
    except Exception as e:
        return f"❌ Ошибка получения списка лабораторных: {e}"


async def handle_scores(lms_client: LMSClient, lab_name: str = "") -> str:
    """Handle /scores command."""
    try:
        if not lab_name:
            return "📊 Укажите название лабораторной: /scores <lab-name>"
        
        analytics = await lms_client.get_analytics()
        if not analytics:
            return "📭 Данные аналитики не найдены"
        
        # Ищем нужную лабораторную в аналитике
        for item in analytics:
            if item.get("item_name", "").lower() == lab_name.lower():
                pass_rate = item.get("pass_rate", 0)
                total = item.get("total_learners", 0)
                passed = item.get("passed_learners", 0)
                return f"📊 Результаты по {lab_name}:\n\nПроцент сдачи: {pass_rate:.1f}%\nСдали: {passed}/{total}"
        
        return f"📭 Лабораторная '{lab_name}' не найдена"
    except Exception as e:
        return f"❌ Ошибка получения результатов: {e}"
