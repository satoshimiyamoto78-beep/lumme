"""
Скрипт для инициализации БД и заполнения тестовыми данными
Запускается при первом запуске приложения на Railway
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app_extended import app, db, User, Seller, Customer, Product, Order, OrderItem, Review, Cart
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Инициализация БД и создание таблиц"""
    with app.app_context():
        print("🔄 Создание таблиц БД...")
        db.create_all()
        print("✅ Таблицы созданы")
        
        # Проверка, есть ли уже данные
        if User.query.first():
            print("⚠️ БД уже содержит данные, пропускаем заполнение")
            return
        
        print("\n📝 Заполнение БД тестовыми данными...")
        
        # ============================================================================
        # СОЗДАНИЕ ПРОДАВЦОВ
        # ============================================================================
        
        sellers_data = [
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
        
        sellers = []
        for seller_data in sellers_data:
            user = User(
                email=seller_data["email"],
                password_hash=generate_password_hash(seller_data["password"]),
                first_name=seller_data["name"].split()[0],
                last_name=seller_data["name"].split()[1] if len(seller_data["name"].split()) > 1 else "",
                phone=seller_data["phone"],
                user_type="seller"
            )
            db.session.add(user)
            db.session.flush()
            
            seller = Seller(
                user_id=user.id,
                shop_name=seller_data["shop_name"],
                shop_address=seller_data["shop_address"],
                shop_description=seller_data["shop_description"],
                rating=5.0
            )
            db.session.add(seller)
            sellers.append(seller)
            print(f"✅ Продавец: {seller_data['name']}")
        
        db.session.commit()
        
        # ============================================================================
        # СОЗДАНИЕ ТОВАРОВ
        # ============================================================================
        
        products_data = [
            {
                "name": "Букет красных роз",
                "price": 350,
                "description": "Прекрасный букет из 15 красных роз",
                "composition": "15 красных роз, зелень",
                "occasion": "love",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет для дня рождения",
                "price": 280,
                "description": "Яркий букет с разноцветными цветами",
                "composition": "Розы, гвоздики, хризантемы",
                "occasion": "birthday",
                "size": "large",
                "in_stock": True
            },
            {
                "name": "Свадебный букет",
                "price": 500,
                "description": "Элегантный букет для невесты",
                "composition": "Белые розы, лилии, зелень",
                "occasion": "wedding",
                "size": "large",
                "in_stock": True
            },
            {
                "name": "Букет тюльпанов",
                "price": 250,
                "description": "Свежие тюльпаны весны",
                "composition": "25 тюльпанов разных цветов",
                "occasion": "congratulations",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет подсолнухов",
                "price": 200,
                "description": "Солнечный букет подсолнухов",
                "composition": "15 подсолнухов, зелень",
                "occasion": "congratulations",
                "size": "small",
                "in_stock": True
            },
            {
                "name": "Букет гвоздик",
                "price": 180,
                "description": "Классический букет красных гвоздик",
                "composition": "20 красных гвоздик",
                "occasion": "love",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет лилий",
                "price": 320,
                "description": "Ароматный букет белых лилий",
                "composition": "10 белых лилий, зелень",
                "occasion": "anniversary",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет орхидей",
                "price": 400,
                "description": "Экзотический букет орхидей",
                "composition": "10 орхидей, зелень",
                "occasion": "congratulations",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет хризантем",
                "price": 220,
                "description": "Яркие хризантемы разных цветов",
                "composition": "30 хризантем, зелень",
                "occasion": "birthday",
                "size": "large",
                "in_stock": True
            },
            {
                "name": "Букет пионов",
                "price": 450,
                "description": "Роскошный букет розовых пионов",
                "composition": "15 пионов, зелень",
                "occasion": "anniversary",
                "size": "large",
                "in_stock": True
            },
            {
                "name": "Букет смешанный",
                "price": 300,
                "description": "Красивый букет из разных цветов",
                "composition": "Розы, гвоздики, альстромерия, зелень",
                "occasion": "congratulations",
                "size": "medium",
                "in_stock": True
            },
            {
                "name": "Букет для юбилея",
                "price": 380,
                "description": "Элегантный букет для торжества",
                "composition": "Розы, лилии, зелень",
                "occasion": "anniversary",
                "size": "large",
                "in_stock": True
            }
        ]
        
        for i, product_data in enumerate(products_data):
            seller = sellers[i % len(sellers)]
            product = Product(
                seller_id=seller.id,
                name=product_data["name"],
                price=product_data["price"],
                description=product_data["description"],
                composition=product_data["composition"],
                occasion=product_data["occasion"],
                size=product_data["size"],
                in_stock=product_data["in_stock"],
                rating=4.5,
                review_count=0
            )
            db.session.add(product)
            print(f"✅ Товар: {product_data['name']}")
        
        db.session.commit()
        
        # ============================================================================
        # СОЗДАНИЕ ПОКУПАТЕЛЕЙ
        # ============================================================================
        
        customers_data = [
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
        
        for customer_data in customers_data:
            user = User(
                email=customer_data["email"],
                password_hash=generate_password_hash(customer_data["password"]),
                first_name=customer_data["name"].split()[0],
                last_name=customer_data["name"].split()[1] if len(customer_data["name"].split()) > 1 else "",
                phone=customer_data["phone"],
                user_type="customer"
            )
            db.session.add(user)
            db.session.flush()
            
            customer = Customer(
                user_id=user.id
            )
            db.session.add(customer)
            print(f"✅ Покупатель: {customer_data['name']}")
        
        db.session.commit()
        
        print("\n" + "=" * 60)
        print("✅ БД инициализирована успешно!")
        print("\n📊 Что было создано:")
        print(f"   • {len(sellers_data)} продавцов")
        print(f"   • {len(products_data)} товаров")
        print(f"   • {len(customers_data)} покупателей")
        print("\n🔐 Тестовые аккаунты:")
        for seller_data in sellers_data:
            print(f"   Продавец: {seller_data['email']} / {seller_data['password']}")
        for customer_data in customers_data:
            print(f"   Покупатель: {customer_data['email']} / {customer_data['password']}")
        print("=" * 60)

if __name__ == '__main__':
    init_database()
