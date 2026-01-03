# 🚀 Развертывание Lumme на Railway и Netlify

Полная инструкция по развертыванию маркетплейса цветов в production.

## 📋 Требования

- GitHub аккаунт
- Railway аккаунт (https://railway.app)
- Netlify аккаунт (https://netlify.com)
- Git установлен локально

---

## 🔧 Подготовка проекта

### 1. Инициализация Git репозитория

```bash
cd /home/ubuntu/lumme-marketplace
git init
git add .
git commit -m "Initial commit: Lumme marketplace MVP"
```

### 2. Создание GitHub репозитория

1. Перейдите на https://github.com/new
2. Создайте новый репозиторий `lumme-marketplace`
3. Не инициализируйте README, .gitignore, license

### 3. Подключение к GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/lumme-marketplace.git
git branch -M main
git push -u origin main
```

---

## 🚂 Развертывание бэкенда на Railway

### Шаг 1: Подготовка файлов

Убедитесь, что в папке `backend/` есть:
- ✅ `app_extended.py` - Главное приложение
- ✅ `requirements.txt` - Зависимости
- ✅ `Procfile` - Инструкции для Railway
- ✅ `runtime.txt` - Версия Python

### Шаг 2: Создание проекта на Railway

1. Перейдите на https://railway.app
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub"
4. Авторизуйте GitHub
5. Выберите репозиторий `lumme-marketplace`
6. Выберите ветку `main`

### Шаг 3: Конфигурация переменных окружения

На Railway добавьте переменные в "Variables":

```
DATABASE_URL=postgresql://user:password@host:port/lumme_db
JWT_SECRET_KEY=your-super-secret-key-here-change-this
TELEGRAM_BOT_TOKEN=8383182287:AAFqF8uDYESA0FVCkW7_-QKYvp4Argd3YqA
TELEGRAM_BOT_USERNAME=LummeOfficial_bot
FLASK_ENV=production
CORS_ORIGINS=*
```

### Шаг 4: Добавление PostgreSQL БД

1. На Railway нажмите "+ Add"
2. Выберите "PostgreSQL"
3. Railway автоматически создаст `DATABASE_URL`
4. Нажмите "Deploy"

### Шаг 5: Инициализация БД

После развертывания:

```bash
# Подключитесь к Railway через SSH или используйте их консоль
python backend/seed_data.py
```

### Результат

Ваш API будет доступен по адресу:
```
https://lumme-api-production.up.railway.app
```

---

## 🌐 Развертывание фронтенда на Netlify

### Шаг 1: Подготовка фронтенда

Обновите URL API в `frontend/index.html` и других файлах:

```javascript
// Замените
const API_BASE_URL = 'http://localhost:5000/api';

// На
const API_BASE_URL = 'https://lumme-api-production.up.railway.app/api';
```

### Шаг 2: Создание проекта на Netlify

1. Перейдите на https://app.netlify.com
2. Нажмите "New site from Git"
3. Выберите GitHub
4. Авторизуйте GitHub
5. Выберите репозиторий `lumme-marketplace`

### Шаг 3: Конфигурация сборки

Установите следующие параметры:

| Параметр | Значение |
| :--- | :--- |
| **Build command** | (оставить пусто) |
| **Publish directory** | `frontend` |

### Шаг 4: Переменные окружения (опционально)

Если используете переменные окружения:

```
REACT_APP_API_URL=https://lumme-api-production.up.railway.app/api
```

### Шаг 5: Развертывание

Нажмите "Deploy site"

### Результат

Ваш фронтенд будет доступен по адресу:
```
https://lumme-marketplace.netlify.app
```

---

## 🤖 Развертывание Telegram бота

### Шаг 1: Создание файла telegram_bot.py

```python
# backend/telegram_bot.py
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
WEB_APP_URL = 'https://lumme-marketplace.netlify.app'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    keyboard = [
        [InlineKeyboardButton(
            "🛍️ Открыть магазин",
            web_app=WebAppInfo(url=WEB_APP_URL)
        )],
        [InlineKeyboardButton(
            "📱 Мой профиль",
            web_app=WebAppInfo(url=f"{WEB_APP_URL}/profile")
        )],
        [InlineKeyboardButton(
            "🛒 Моя корзина",
            web_app=WebAppInfo(url=f"{WEB_APP_URL}/cart")
        )]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 Добро пожаловать в Lumme!\n\n"
        "Лучший маркетплейс цветов в Таджикистане.\n\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /shop"""
    keyboard = [[InlineKeyboardButton(
        "🛍️ Перейти в магазин",
        web_app=WebAppInfo(url=WEB_APP_URL)
    )]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🌸 Откройте наш магазин и выберите красивый букет!",
        reply_markup=reply_markup
    )

def main():
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("shop", shop))
    
    application.run_polling()

if __name__ == '__main__':
    main()
```

### Шаг 2: Запуск бота

```bash
cd backend
pip install python-telegram-bot
python telegram_bot.py
```

---

## 🔗 Интеграция Telegram Web App

### В index.html добавьте:

```html
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<script>
    // Инициализация Telegram Web App
    window.Telegram.WebApp.ready();
    const tg = window.Telegram.WebApp;
    
    // Получение данных пользователя
    const user = tg.initDataUnsafe.user;
    if (user) {
        console.log('Telegram user:', user);
        // Автоматический вход через Telegram
        // TODO: Реализовать вход через Telegram ID
    }
    
    // Закрытие Web App
    function closeApp() {
        tg.close();
    }
</script>
```

---

## ✅ Проверка развертывания

### 1. Проверка API

```bash
curl https://lumme-api-production.up.railway.app/api/health
```

Ожидаемый ответ:
```json
{
    "status": "ok",
    "message": "Lumme API is running",
    "version": "1.0.0"
}
```

### 2. Проверка фронтенда

Откройте в браузере:
```
https://lumme-marketplace.netlify.app
```

### 3. Проверка Telegram бота

1. Откройте Telegram
2. Найдите @LummeOfficial_bot
3. Отправьте `/start`
4. Нажмите на кнопку "Открыть магазин"

---

## 🔐 Безопасность в Production

### 1. Обновите JWT_SECRET_KEY

```bash
# Генерируйте новый секретный ключ
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Установите его в Railway переменных окружения.

### 2. Включите HTTPS

Railway и Netlify автоматически используют HTTPS.

### 3. Обновите CORS

В `backend/app_extended.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://lumme-marketplace.netlify.app"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### 4. Установите рейты лимиты

```bash
pip install Flask-Limiter
```

---

## 📊 Мониторинг

### Railway Dashboard

1. Перейдите на https://railway.app/dashboard
2. Выберите ваш проект
3. Смотрите логи в реальном времени

### Netlify Analytics

1. Перейдите на https://app.netlify.com
2. Выберите ваш сайт
3. Смотрите аналитику в "Analytics"

---

## 🐛 Решение проблем

### Ошибка: "DATABASE_URL не установлена"

```bash
# Проверьте переменные в Railway
railway variables
```

### Ошибка: "CORS блокирует запросы"

Убедитесь, что в `backend/app_extended.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Ошибка: "Telegram Web App не открывается"

1. Проверьте, что фронтенд доступен по HTTPS
2. Проверьте WEB_APP_URL в telegram_bot.py
3. Перезагрузите бота

---

## 🎉 Готово!

Ваш маркетплейс Lumme теперь в production!

**Ссылки:**
- 🌐 Веб-сайт: https://lumme-marketplace.netlify.app
- 🔌 API: https://lumme-api-production.up.railway.app
- 🤖 Telegram бот: https://t.me/LummeOfficial_bot

---

## 📞 Поддержка

Если у вас есть проблемы:

1. Проверьте логи на Railway
2. Проверьте консоль браузера (F12)
3. Прочитайте документацию Railway и Netlify
4. Свяжитесь с поддержкой

---

**Создано с ❤️ для Таджикистана**
