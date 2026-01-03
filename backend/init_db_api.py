"""
Скрипт для инициализации БД через API
Используется для заполнения тестовыми данными на Railway
"""

import requests
import json
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# API URL
API_URL = os.getenv('API_URL', 'https://lumme-production.up.railway.app/api')

print(f"🌐 Подключение к API: {API_URL}")
print("=" * 60)

# ============================================================================
# РЕГИСТРАЦИЯ ПРОДАВЦОВ
# ============================================================================

sellers = [
    {
        "email": "florist1@lumme.tj",
        "password": "password123",
        "name": "Фарход Цветочный",
        "phone": "+992 37 227-00-01",
        "shop_name": "Цветочная лавка №1",
        "shop_address": "Душанбе, ул. Айни, 45",
        "shop_description": "Лучший выбор букетов в городе"
    },
    {
        "email": "florist2@lumme.tj",
        "password": "password123",
        "name": "Гульнора Розовая",
        "phone": "+992 37 227-00-02",
        "shop_name": "Розовая мечта",
        "shop_address": "Душанбе, ул. Рудаки, 78",
        "shop_description": "Свежие цветы каждый день"
    }
]

seller_tokens = []

print("\n📝 Регистрация продавцов...")
for seller in sellers:
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": seller["email"],
                "password": seller["password"],
                "name": seller["name"],
                "phone": seller["phone"],
                "shop_name": seller["shop_name"],
                "shop_address": seller["shop_address"],
                "shop_description": seller["shop_description"],
                "user_type": "seller"
            }
        )
        
        if response.status_code == 201 or response.status_code == 200:
            data = response.json()
            token = data.get('token') or data.get('access_token')
            seller_tokens.append(token)
            print(f"✅ {seller['name']} зарегистрирован")
        else:
            print(f"⚠️ {seller['name']}: {response.text}")
            # Попытка входа
            login_response = requests.post(
                f"{API_URL}/auth/login",
                json={"email": seller["email"], "password": seller["password"]}
            )
            if login_response.status_code == 200:
                data = login_response.json()
                token = data.get('token') or data.get('access_token')
                seller_tokens.append(token)
                print(f"✅ {seller['name']} вошел в систему")
    except Exception as e:
        print(f"❌ Ошибка при регистрации {seller['name']}: {e}")

# ============================================================================
# СОЗДАНИЕ ТОВАРОВ
# ============================================================================

products = [
    {
        "name": "Букет красных роз",
        "price": 350,
        "description": "Прекрасный букет из 15 красных роз",
        "composition": "15 красных роз, зелень",
        "occasion": "love",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Red+Roses",
        "in_stock": True
    },
    {
        "name": "Букет для дня рождения",
        "price": 280,
        "description": "Яркий букет с разноцветными цветами",
        "composition": "Розы, гвоздики, хризантемы",
        "occasion": "birthday",
        "size": "large",
        "image_url": "https://via.placeholder.com/300x300?text=Birthday",
        "in_stock": True
    },
    {
        "name": "Свадебный букет",
        "price": 500,
        "description": "Элегантный букет для невесты",
        "composition": "Белые розы, лилии, зелень",
        "occasion": "wedding",
        "size": "large",
        "image_url": "https://via.placeholder.com/300x300?text=Wedding",
        "in_stock": True
    },
    {
        "name": "Букет тюльпанов",
        "price": 250,
        "description": "Свежие тюльпаны весны",
        "composition": "25 тюльпанов разных цветов",
        "occasion": "congratulations",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Tulips",
        "in_stock": True
    },
    {
        "name": "Букет подсолнухов",
        "price": 200,
        "description": "Солнечный букет подсолнухов",
        "composition": "15 подсолнухов, зелень",
        "occasion": "congratulations",
        "size": "small",
        "image_url": "https://via.placeholder.com/300x300?text=Sunflowers",
        "in_stock": True
    },
    {
        "name": "Букет гвоздик",
        "price": 180,
        "description": "Классический букет красных гвоздик",
        "composition": "20 красных гвоздик",
        "occasion": "love",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Carnations",
        "in_stock": True
    },
    {
        "name": "Букет лилий",
        "price": 320,
        "description": "Ароматный букет белых лилий",
        "composition": "10 белых лилий, зелень",
        "occasion": "anniversary",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Lilies",
        "in_stock": True
    },
    {
        "name": "Букет орхидей",
        "price": 400,
        "description": "Экзотический букет орхидей",
        "composition": "10 орхидей, зелень",
        "occasion": "congratulations",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Orchids",
        "in_stock": True
    },
    {
        "name": "Букет хризантем",
        "price": 220,
        "description": "Яркие хризантемы разных цветов",
        "composition": "30 хризантем, зелень",
        "occasion": "birthday",
        "size": "large",
        "image_url": "https://via.placeholder.com/300x300?text=Chrysanthemums",
        "in_stock": True
    },
    {
        "name": "Букет пионов",
        "price": 450,
        "description": "Роскошный букет розовых пионов",
        "composition": "15 пионов, зелень",
        "occasion": "anniversary",
        "size": "large",
        "image_url": "https://via.placeholder.com/300x300?text=Peonies",
        "in_stock": True
    },
    {
        "name": "Букет смешанный",
        "price": 300,
        "description": "Красивый букет из разных цветов",
        "composition": "Розы, гвоздики, альстромерия, зелень",
        "occasion": "congratulations",
        "size": "medium",
        "image_url": "https://via.placeholder.com/300x300?text=Mixed",
        "in_stock": True
    },
    {
        "name": "Букет для юбилея",
        "price": 380,
        "description": "Элегантный букет для торжества",
        "composition": "Розы, лилии, зелень",
        "occasion": "anniversary",
        "size": "large",
        "image_url": "https://via.placeholder.com/300x300?text=Anniversary",
        "in_stock": True
    }
]

print("\n🌹 Создание товаров...")
for i, product in enumerate(products):
    if i < len(seller_tokens):
        seller_token = seller_tokens[i % len(seller_tokens)]
        try:
            response = requests.post(
                f"{API_URL}/products",
                json=product,
                headers={"Authorization": f"Bearer {seller_token}"}
            )
            
            if response.status_code == 201 or response.status_code == 200:
                print(f"✅ {product['name']}")
            else:
                print(f"⚠️ {product['name']}: {response.text}")
        except Exception as e:
            print(f"❌ Ошибка при создании {product['name']}: {e}")

# ============================================================================
# РЕГИСТРАЦИЯ ПОКУПАТЕЛЕЙ
# ============================================================================

customers = [
    {
        "email": "customer1@lumme.tj",
        "password": "password123",
        "name": "Зарина Покупатель",
        "phone": "+992 37 227-00-10"
    },
    {
        "email": "customer2@lumme.tj",
        "password": "password123",
        "name": "Махмуд Клиент",
        "phone": "+992 37 227-00-11"
    }
]

print("\n👥 Регистрация покупателей...")
for customer in customers:
    try:
        response = requests.post(
            f"{API_URL}/auth/register",
            json={
                "email": customer["email"],
                "password": customer["password"],
                "name": customer["name"],
                "phone": customer["phone"],
                "user_type": "customer"
            }
        )
        
        if response.status_code == 201 or response.status_code == 200:
            print(f"✅ {customer['name']} зарегистрирован")
        else:
            print(f"⚠️ {customer['name']}: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка при регистрации {customer['name']}: {e}")

# ============================================================================
# ИТОГИ
# ============================================================================

print("\n" + "=" * 60)
print("✅ Инициализация БД завершена!")
print("\n📊 Что было создано:")
print(f"   • {len(sellers)} продавцов")
print(f"   • {len(products)} товаров")
print(f"   • {len(customers)} покупателей")
print("\n🔐 Тестовые аккаунты:")
print("   Продавец 1: florist1@lumme.tj / password123")
print("   Продавец 2: florist2@lumme.tj / password123")
print("   Покупатель 1: customer1@lumme.tj / password123")
print("   Покупатель 2: customer2@lumme.tj / password123")
print("\n🌐 API: " + API_URL)
print("=" * 60)
