"""
Lumme - Маркетплейс цветов
Главное приложение Flask
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from datetime import timedelta

# Загрузка переменных окружения
load_dotenv()

# Инициализация Flask приложения
app = Flask(__name__)

# Конфигурация
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost:5432/lumme_db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Инициализация расширений
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ============================================================================
# МОДЕЛИ ДАННЫХ
# ============================================================================

class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20), default='customer')  # customer, seller, admin
    telegram_id = db.Column(db.BigInteger, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Отношения
    seller = db.relationship('Seller', backref='user', uselist=False, cascade='all, delete-orphan')
    customer = db.relationship('Customer', backref='user', uselist=False, cascade='all, delete-orphan')


class Seller(db.Model):
    """Модель профиля продавца"""
    __tablename__ = 'sellers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    shop_name = db.Column(db.String(255), nullable=False)
    shop_description = db.Column(db.Text)
    shop_address = db.Column(db.String(255))
    shop_phone = db.Column(db.String(20))
    rating = db.Column(db.Float, default=0.0)
    total_sales = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Отношения
    products = db.relationship('Product', backref='seller', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='seller', cascade='all, delete-orphan')


class Customer(db.Model):
    """Модель профиля покупателя"""
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    default_address = db.Column(db.String(255))
    delivery_addresses = db.Column(db.JSON, default=[])
    total_orders = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Отношения
    orders = db.relationship('Order', backref='customer', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='customer', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='customer', cascade='all, delete-orphan')


class Product(db.Model):
    """Модель товара (букета)"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    composition = db.Column(db.JSON)  # {roses: 7, carnations: 5}
    occasion = db.Column(db.String(100))  # День рождения, Свадьба и т.д.
    size = db.Column(db.String(20), default='medium')  # small, medium, large
    stock_quantity = db.Column(db.Integer, default=0)
    is_in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Отношения
    order_items = db.relationship('OrderItem', backref='product', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='product', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', cascade='all, delete-orphan')


class Order(db.Model):
    """Модель заказа"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    delivery_time = db.Column(db.String(20))
    personal_message = db.Column(db.Text)
    payment_method = db.Column(db.String(50), default='cash_on_delivery')
    order_status = db.Column(db.String(50), default='pending')  # pending, confirmed, preparing, on_the_way, delivered, cancelled
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    # Отношения
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='order', cascade='all, delete-orphan')


class OrderItem(db.Model):
    """Модель товара в заказе"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Review(db.Model):
    """Модель отзыва"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Cart(db.Model):
    """Модель корзины"""
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='unique_cart_item'),)


# ============================================================================
# API МАРШРУТЫ
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья приложения"""
    return jsonify({
        'status': 'ok',
        'message': 'Lumme API is running',
        'version': '1.0.0'
    }), 200


@app.route('/api/products', methods=['GET'])
def get_products():
    """Получить все товары с фильтрацией"""
    try:
        # Параметры фильтрации
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        occasion = request.args.get('occasion', None)
        size = request.args.get('size', None)
        min_price = request.args.get('min_price', 0, type=float)
        max_price = request.args.get('max_price', float('inf'), type=float)
        
        # Базовый запрос
        query = Product.query.filter(Product.is_in_stock == True)
        
        # Применение фильтров
        if occasion:
            query = query.filter(Product.occasion == occasion)
        if size:
            query = query.filter(Product.size == size)
        
        query = query.filter(
            Product.price >= min_price,
            Product.price <= max_price
        )
        
        # Пагинация
        products = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [{
                'id': p.id,
                'name': p.name,
                'price': p.price,
                'description': p.description,
                'image_url': p.image_url,
                'rating': p.rating,
                'review_count': p.review_count,
                'size': p.size,
                'occasion': p.occasion,
                'seller': {
                    'id': p.seller.id,
                    'shop_name': p.seller.shop_name,
                    'rating': p.seller.rating
                }
            } for p in products.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': products.total,
                'pages': products.pages
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить детали товара"""
    try:
        product = Product.query.get_or_404(product_id)
        
        return jsonify({
            'success': True,
            'data': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'description': product.description,
                'composition': product.composition,
                'occasion': product.occasion,
                'size': product.size,
                'stock_quantity': product.stock_quantity,
                'is_in_stock': product.is_in_stock,
                'image_url': product.image_url,
                'rating': product.rating,
                'review_count': product.review_count,
                'seller': {
                    'id': product.seller.id,
                    'shop_name': product.seller.shop_name,
                    'shop_description': product.seller.shop_description,
                    'rating': product.seller.rating
                }
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Обработка ошибки 404"""
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Обработка ошибки 500"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


# ============================================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ База данных инициализирована")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
