"""
Telegram Bot для Lumme маркетплейса
Интеграция с Web App для открытия магазина в Telegram
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.constants import ChatAction
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Конфигурация логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8383182287:AAFqF8uDYESA0FVCkW7_-QKYvp4Argd3YqA')
WEB_APP_URL = os.getenv('WEB_APP_URL', 'https://lummu.netlify.app')
API_URL = os.getenv('API_URL', 'https://lumme-production.up.railway.app/api')

# ============================================================================
# КОМАНДЫ БОТА
# ============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /start - Главное меню
    """
    user = update.effective_user
    
    # Создание клавиатуры с Web App кнопками
    keyboard = [
        [InlineKeyboardButton(
            "🛍️ Открыть магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [
            InlineKeyboardButton(
                "📱 Мой профиль",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}/profile")
            ),
            InlineKeyboardButton(
                "🛒 Моя корзина",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}/cart")
            )
        ],
        [
            InlineKeyboardButton(
                "📋 Мои заказы",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}/orders")
            ),
            InlineKeyboardButton(
                "❓ Помощь",
                callback_data="help"
            )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        f"🌸 Привет, {user.first_name}!\n\n"
        "Добро пожаловать в **Lumme** - лучший маркетплейс цветов в Таджикистане!\n\n"
        "✨ Здесь вы найдете:\n"
        "🌹 Красивые букеты на любой случай\n"
        "🎁 Подарки и аксессуары\n"
        "💝 Быструю доставку\n"
        "⭐ Качественное обслуживание\n\n"
        "Выберите действие ниже:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /shop - Открыть магазин
    """
    keyboard = [[InlineKeyboardButton(
        "🛍️ Перейти в магазин",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 Откройте наш магазин и выберите красивый букет!\n\n"
        "Нажмите кнопку ниже, чтобы начать покупки:",
        reply_markup=reply_markup
    )


async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /catalog - Каталог товаров
    """
    keyboard = [
        [InlineKeyboardButton(
            "🌹 Все букеты",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [
            InlineKeyboardButton(
                "🎂 День рождения",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}?occasion=birthday")
            ),
            InlineKeyboardButton(
                "💒 Свадьба",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}?occasion=wedding")
            )
        ],
        [
            InlineKeyboardButton(
                "🎉 Поздравления",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}?occasion=congratulations")
            ),
            InlineKeyboardButton(
                "💐 Юбилей",
                web_app=WebAppInfo(url=f"{WEB_APP_URL}?occasion=anniversary")
            )
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📚 Выберите категорию букетов:",
        reply_markup=reply_markup
    )


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /orders - Мои заказы
    """
    keyboard = [[InlineKeyboardButton(
        "📋 Посмотреть заказы",
        web_app=WebAppInfo(url=f"{WEB_APP_URL}/orders")
    )]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "📦 Откройте страницу ваших заказов:",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /help - Справка
    """
    help_text = (
        "❓ **Справка по командам:**\n\n"
        "/start - Главное меню\n"
        "/shop - Открыть магазин\n"
        "/catalog - Каталог букетов\n"
        "/orders - Мои заказы\n"
        "/help - Эта справка\n\n"
        "**Часто задаваемые вопросы:**\n\n"
        "❓ Как оформить заказ?\n"
        "Откройте магазин, выберите букет, добавьте в корзину и оформите заказ.\n\n"
        "❓ Какие способы оплаты доступны?\n"
        "Наличные при доставке и банковские карты.\n\n"
        "❓ Как долго доставляется заказ?\n"
        "Обычно 1-2 часа в пределах города.\n\n"
        "❓ Могу ли я отменить заказ?\n"
        "Да, если заказ еще не в пути. Свяжитесь с поддержкой.\n\n"
        "📞 **Контакты поддержки:**\n"
        "Telegram: @LummeSupport\n"
        "Email: support@lumme.tj\n"
        "Телефон: +992 (37) 227-00-00"
    )
    
    await update.message.reply_text(
        help_text,
        parse_mode='Markdown'
    )


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Команда /about - О компании
    """
    about_text = (
        "🌸 **О Lumme**\n\n"
        "Lumme - это современный маркетплейс цветов в Таджикистане.\n\n"
        "✨ **Наши преимущества:**\n"
        "🌹 Большой выбор букетов\n"
        "🚚 Быстрая доставка\n"
        "💯 Качество гарантировано\n"
        "⭐ Отличные отзывы\n"
        "💝 Персональный подход\n\n"
        "📍 **Где мы находимся:**\n"
        "Душанбе, Таджикистан\n\n"
        "🌐 **Веб-сайт:** lumme.tj\n"
        "📱 **Telegram:** @LummeOfficial_bot"
    )
    
    await update.message.reply_text(
        about_text,
        parse_mode='Markdown'
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработка обычных сообщений
    """
    user_message = update.message.text.lower()
    
    # Простой поиск по ключевым словам
    if 'привет' in user_message or 'привет' in user_message:
        await update.message.reply_text(
            "👋 Привет! Используйте /start для главного меню или /help для справки."
        )
    elif 'цена' in user_message or 'стоимость' in user_message:
        await update.message.reply_text(
            "💰 Цены на букеты варьируются от 200 до 1000 сомони.\n"
            "Откройте магазин, чтобы увидеть все цены: /shop"
        )
    elif 'доставка' in user_message:
        await update.message.reply_text(
            "🚚 Доставка доступна в пределах города.\n"
            "Стоимость доставки: 50 сомони\n"
            "Время доставки: 1-2 часа"
        )
    else:
        await update.message.reply_text(
            "Я не совсем понял. 🤔\n\n"
            "Используйте команды:\n"
            "/start - Главное меню\n"
            "/shop - Магазин\n"
            "/help - Справка"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обработчик ошибок
    """
    logger.error(f"Update {update} caused error {context.error}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main() -> None:
    """
    Запуск бота
    """
    # Создание приложения
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shop", shop))
    application.add_handler(CommandHandler("catalog", catalog))
    application.add_handler(CommandHandler("orders", orders))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    
    # Добавление обработчика сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавление обработчика ошибок
    application.add_error_handler(error_handler)
    
    # Запуск бота
    print("🤖 Telegram бот запущен!")
    print(f"🌐 Web App URL: {WEB_APP_URL}")
    print(f"🔌 API URL: {API_URL}")
    print("\nОтправьте /start для тестирования")
    
    application.run_polling()


if __name__ == '__main__':
    main()
