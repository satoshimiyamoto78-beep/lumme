"""
Скрипт для заполнения БД тестовыми данными
"""

from app_extended import app, db, User, Seller, Customer, Product
from datetime import datetime

def seed_database():
    """Заполнить БД тестовыми данными"""
    
    with app.app_context():
        # Очистка БД
        db.drop_all()
        db.create_all()
        print("✅ База данных очищена и пересоздана")
        
        # Создание тестовых продавцов
        sellers_data = [
            {
                'email': 'florist1@lumme.tj',
                'password': 'password123',
                'first_name': 'Фарход',
                'last_name': 'Хамидов',
                'phone': '+992 (37) 227-00-01',
                'shop_name': 'Цветочный рай',
                'shop_description': 'Лучшие букеты в городе',
                'shop_address': 'ул. Айни, 123, Душанбе'
            },
            {
                'email': 'florist2@lumme.tj',
                'password': 'password123',
                'first_name': 'Зарина',
                'last_name': 'Мирова',
                'phone': '+992 (37) 227-00-02',
                'shop_name': 'Розовая мечта',
                'shop_description': 'Специализируемся на розах',
                'shop_address': 'ул. Сомони, 456, Душанбе'
            }
        ]
        
        sellers = []
        for seller_data in sellers_data:
            user = User(
                email=seller_data['email'],
                first_name=seller_data['first_name'],
                last_name=seller_data['last_name'],
                phone=seller_data['phone'],
                user_type='seller'
            )
            user.set_password(seller_data['password'])
            db.session.add(user)
            db.session.flush()
            
            seller = Seller(
                user_id=user.id,
                shop_name=seller_data['shop_name'],
                shop_description=seller_data['shop_description'],
                shop_address=seller_data['shop_address'],
                shop_phone=seller_data['phone'],
                rating=4.5,
                is_verified=True
            )
            db.session.add(seller)
            sellers.append(seller)
        
        db.session.commit()
        print(f"✅ Создано {len(sellers)} продавцов")
        
        # Создание тестовых товаров
        products_data = [
            {
                'name': 'Букет красных роз',
                'description': 'Прекрасный букет из 25 красных роз',
                'price': 450,
                'composition': {'roses': 25, 'greenery': 5},
                'occasion': 'birthday',
                'size': 'large',
                'stock_quantity': 10,
                'image_url': 'https://images.unsplash.com/photo-1518895949257-7621c3c786d7?w=500'
            },
            {
                'name': 'Букет пионов',
                'description': 'Нежный букет из пионов',
                'price': 350,
                'composition': {'peonies': 15, 'greenery': 3},
                'occasion': 'anniversary',
                'size': 'medium',
                'stock_quantity': 8,
                'image_url': 'https://images.unsplash.com/photo-1520763185298-1b434c919abe?w=500'
            },
            {
                'name': 'Букет тюльпанов',
                'description': 'Яркий букет из разноцветных тюльпанов',
                'price': 300,
                'composition': {'tulips': 20, 'greenery': 4},
                'occasion': 'congratulations',
                'size': 'medium',
                'stock_quantity': 15,
                'image_url': 'https://images.unsplash.com/photo-1561181286-d3fee7d55364?w=500'
            },
            {
                'name': 'Букет гвоздик',
                'description': 'Классический букет из гвоздик',
                'price': 250,
                'composition': {'carnations': 30, 'greenery': 5},
                'occasion': 'birthday',
                'size': 'small',
                'stock_quantity': 20,
                'image_url': 'https://images.unsplash.com/photo-1563241527-3004a5e5e313?w=500'
            },
            {
                'name': 'Букет подсолнухов',
                'description': 'Солнечный букет из подсолнухов',
                'price': 280,
                'composition': {'sunflowers': 7, 'greenery': 3},
                'occasion': 'congratulations',
                'size': 'large',
                'stock_quantity': 6,
                'image_url': 'https://images.unsplash.com/photo-1597848848222-e2d5b5c45d0f?w=500'
            },
            {
                'name': 'Букет лилий',
                'description': 'Элегантный букет из лилий',
                'price': 400,
                'composition': {'lilies': 12, 'greenery': 4},
                'occasion': 'wedding',
                'size': 'large',
                'stock_quantity': 5,
                'image_url': 'https://images.unsplash.com/photo-1563241527-3004a5e5e313?w=500'
            }
        ]
        
        product_count = 0
        for seller in sellers:
            for product_data in products_data:
                product = Product(
                    seller_id=seller.id,
                    name=product_data['name'],
                    description=product_data['description'],
                    price=product_data['price'],
                    composition=product_data['composition'],
                    occasion=product_data['occasion'],
                    size=product_data['size'],
                    stock_quantity=product_data['stock_quantity'],
                    is_in_stock=True,
                    image_url=product_data['image_url'],
                    rating=4.7,
                    review_count=5
                )
                db.session.add(product)
                product_count += 1
        
        db.session.commit()
        print(f"✅ Создано {product_count} товаров")
        
        # Создание тестовых покупателей
        customers_data = [
            {
                'email': 'customer1@lumme.tj',
                'password': 'password123',
                'first_name': 'Рахим',
                'last_name': 'Абдуллаев',
                'phone': '+992 (37) 227-00-10'
            },
            {
                'email': 'customer2@lumme.tj',
                'password': 'password123',
                'first_name': 'Наталья',
                'last_name': 'Петрова',
                'phone': '+992 (37) 227-00-11'
            }
        ]
        
        for customer_data in customers_data:
            user = User(
                email=customer_data['email'],
                first_name=customer_data['first_name'],
                last_name=customer_data['last_name'],
                phone=customer_data['phone'],
                user_type='customer'
            )
            user.set_password(customer_data['password'])
            db.session.add(user)
            db.session.flush()
            
            customer = Customer(user_id=user.id)
            db.session.add(customer)
        
        db.session.commit()
        print(f"✅ Создано {len(customers_data)} покупателей")
        
        print("\n✅ БД успешно заполнена тестовыми данными!")
        print("\nТестовые аккаунты:")
        print("Продавец 1: florist1@lumme.tj / password123")
        print("Продавец 2: florist2@lumme.tj / password123")
        print("Покупатель 1: customer1@lumme.tj / password123")
        print("Покупатель 2: customer2@lumme.tj / password123")


if __name__ == '__main__':
    seed_database()
