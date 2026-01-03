# 🚀 Быстрый старт Lumme

Полная инструкция по запуску маркетплейса цветов локально и в production.

---

## 💻 Локальный запуск (Разработка)

### Требования

- Python 3.11+
- PostgreSQL 12+
- Git
- Node.js (опционально)

### Шаг 1: Клонирование репозитория

```bash
git clone https://github.com/YOUR_USERNAME/lumme-marketplace.git
cd lumme-marketplace
```

### Шаг 2: Установка зависимостей бэкенда

```bash
cd backend
python -m venv venv

# На Windows:
venv\Scripts\activate

# На macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Шаг 3: Создание .env файла

```bash
cp .env.example .env
```

Отредактируйте `.env`:

```env
# База данных
DATABASE_URL=postgresql://user:password@localhost:5432/lumme_db
SQLALCHEMY_ECHO=True

# JWT
JWT_SECRET_KEY=your-secret-key-here

# Telegram
TELEGRAM_BOT_TOKEN=8383182287:AAFqF8uDYESA0FVCkW7_-QKYvp4Argd3YqA
TELEGRAM_BOT_USERNAME=LummeOfficial_bot

# Приложение
FLASK_ENV=development
DEBUG=True
```

### Шаг 4: Инициализация БД

```bash
# Создание таблиц
python -c "from app_extended import app, db; app.app_context().push(); db.create_all(); print('✅ БД создана')"

# Заполнение тестовыми данными
python seed_data.py
```

### Шаг 5: Запуск бэкенда

```bash
python app_extended.py
```

Вы должны увидеть:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Шаг 6: Открытие фронтенда

В новом терминале откройте фронтенд:

```bash
# Вариант 1: Простой HTTP сервер (Python)
cd ../frontend
python -m http.server 8000

# Вариант 2: Использование Live Server (VS Code)
# Установите расширение "Live Server"
# Кликните правой кнопкой на index.html → "Open with Live Server"
```

Откройте в браузере:
```
http://localhost:8000
```

### Шаг 7: Запуск Telegram бота (опционально)

```bash
cd backend
python telegram_bot.py
```

---

## 🧪 Тестирование локально

### Тестовые аккаунты

```
Продавец 1:
Email: florist1@lumme.tj
Пароль: password123

Продавец 2:
Email: florist2@lumme.tj
Пароль: password123

Покупатель 1:
Email: customer1@lumme.tj
Пароль: password123

Покупатель 2:
Email: customer2@lumme.tj
Пароль: password123
```

### Проверка API

```bash
# Проверка здоровья
curl http://localhost:5000/api/health

# Получить все товары
curl http://localhost:5000/api/products

# Получить товар по ID
curl http://localhost:5000/api/products/1

# Вход
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "customer1@lumme.tj", "password": "password123"}'
```

---

## 📦 Развертывание в Production

### Вариант 1: Railway (Рекомендуется)

#### Шаг 1: Подготовка

```bash
# Убедитесь, что все файлы в Git
git add .
git commit -m "Ready for deployment"
git push origin main
```

#### Шаг 2: Создание проекта на Railway

1. Перейдите на https://railway.app
2. Нажмите "New Project"
3. Выберите "Deploy from GitHub"
4. Авторизуйте GitHub
5. Выберите репозиторий `lumme-marketplace`

#### Шаг 3: Конфигурация

На Railway добавьте переменные:

```
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=your-production-secret-key
TELEGRAM_BOT_TOKEN=8383182287:AAFqF8uDYESA0FVCkW7_-QKYvp4Argd3YqA
FLASK_ENV=production
```

#### Шаг 4: Добавление PostgreSQL

1. Нажмите "+ Add"
2. Выберите "PostgreSQL"
3. Railway автоматически создаст `DATABASE_URL`

#### Шаг 5: Развертывание

Railway автоматически развернет приложение. Вы получите URL:

```
https://lumme-api-production.up.railway.app
```

---

### Вариант 2: Netlify (Фронтенд)

#### Шаг 1: Подготовка

Обновите API URL в `frontend/index.html`:

```javascript
// Замените
const API_BASE_URL = 'http://localhost:5000/api';

// На
const API_BASE_URL = 'https://lumme-api-production.up.railway.app/api';
```

#### Шаг 2: Развертывание

1. Перейдите на https://app.netlify.com
2. Нажмите "New site from Git"
3. Выберите GitHub и авторизуйтесь
4. Выберите репозиторий `lumme-marketplace`
5. Установите:
   - Build command: (оставить пусто)
   - Publish directory: `frontend`
6. Нажмите "Deploy site"

Вы получите URL:
```
https://lumme-marketplace.netlify.app
```

---

## 🤖 Запуск Telegram бота

### Локально

```bash
cd backend
python telegram_bot.py
```

### На Railway

1. Создайте новый сервис на Railway
2. Выберите "Deploy from GitHub"
3. Выберите ту же ветку
4. Установите команду запуска:
   ```
   python backend/telegram_bot.py
   ```
5. Добавьте переменные окружения (как для API)
6. Развертните

---

## 🔍 Проверка развертывания

### API Health Check

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

### Фронтенд

Откройте в браузере:
```
https://lumme-marketplace.netlify.app
```

### Telegram бот

1. Откройте Telegram
2. Найдите @LummeOfficial_bot
3. Отправьте `/start`
4. Нажмите "🛍️ Открыть магазин"

---

## 📊 Мониторинг и Логи

### Railway Логи

```bash
# Установите Railway CLI
npm install -g @railway/cli

# Логин
railway login

# Просмотр логов
railway logs
```

### Netlify Логи

1. Перейдите на https://app.netlify.com
2. Выберите ваш сайт
3. Откройте "Deploys"
4. Нажмите на последний deploy
5. Откройте "Deploy log"

---

## 🐛 Решение проблем

### Ошибка: "DATABASE_URL не установлена"

```bash
# Проверьте переменные
railway variables

# Или на Railway Dashboard
# Settings → Variables
```

### Ошибка: "CORS блокирует запросы"

Убедитесь, что в `backend/app_extended.py`:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Ошибка: "Telegram Web App не открывается"

1. Убедитесь, что фронтенд доступен по HTTPS
2. Проверьте WEB_APP_URL в `telegram_bot.py`
3. Перезагрузите бота

### Ошибка: "Товары не загружаются"

1. Проверьте, что БД инициализирована: `python seed_data.py`
2. Проверьте логи API: `railway logs`
3. Проверьте консоль браузера (F12)

---

## 📝 Полезные команды

### Локальная разработка

```bash
# Активация виртуального окружения
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Запуск бэкенда
python app_extended.py

# Запуск фронтенда
python -m http.server 8000

# Запуск Telegram бота
python telegram_bot.py

# Заполнение БД тестовыми данными
python seed_data.py
```

### Git команды

```bash
# Добавление изменений
git add .

# Коммит
git commit -m "Описание изменений"

# Отправка на GitHub
git push origin main

# Просмотр статуса
git status
```

### Railway команды

```bash
# Логин
railway login

# Просмотр логов
railway logs

# Просмотр переменных
railway variables

# Просмотр статуса
railway status
```

---

## 🎯 Чек-лист запуска

### Локально

- [ ] Клонирован репозиторий
- [ ] Установлены зависимости
- [ ] Создан .env файл
- [ ] БД инициализирована
- [ ] Бэкенд запущен на http://localhost:5000
- [ ] Фронтенд запущен на http://localhost:8000
- [ ] Можно войти с тестовыми аккаунтами
- [ ] Товары отображаются
- [ ] Корзина работает

### Production

- [ ] Репозиторий на GitHub
- [ ] Railway проект создан
- [ ] PostgreSQL БД добавлена
- [ ] Переменные окружения установлены
- [ ] API развернут и доступен
- [ ] Netlify сайт создан
- [ ] Фронтенд развернут и доступен
- [ ] Telegram бот запущен
- [ ] Web App открывается в Telegram
- [ ] Все функции работают

---

## 📞 Поддержка

Если у вас есть проблемы:

1. Проверьте логи (Railway или консоль браузера)
2. Прочитайте документацию в DEPLOYMENT.md
3. Проверьте README.md
4. Свяжитесь с поддержкой Railway или Netlify

---

## 🎉 Готово!

Ваш маркетплейс Lumme готов к использованию!

**Ссылки:**
- 🌐 Веб-сайт: https://lumme-marketplace.netlify.app
- 🔌 API: https://lumme-api-production.up.railway.app
- 🤖 Telegram: https://t.me/LummeOfficial_bot

---

**Создано с ❤️ для Таджикистана**
