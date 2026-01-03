"""
Lumme - Маркетплейс цветов
Расширенное приложение Flask с полным API
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import uuid
from functools import wraps

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
# МОДЕЛИ ДАННЫХ (из app.py)
# ============================================================================

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    user_type = db.Column(db.String(20), default='customer')
    telegram_id = db.Column(db.BigInteger, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    seller = db.relationship('Seller', backref='user', uselist=False, cascade='all, delete-orphan')
    customer = db.relationship('Customer', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Seller(db.Model):
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
    
    products = db.relationship('Product', backref='seller', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='seller', cascade='all, delete-orphan')


class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    default_address = db.Column(db.String(255))
    delivery_addresses = db.Column(db.JSON, default=[])
    total_orders = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    orders = db.relationship('Order', backref='customer', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='customer', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='customer', cascade='all, delete-orphan')


class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    composition = db.Column(db.JSON)
    occasion = db.Column(db.String(100))
    size = db.Column(db.String(20), default='medium')
    stock_quantity = db.Column(db.Integer, default=0)
    is_in_stock = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    order_items = db.relationship('OrderItem', backref='product', cascade='all, delete-orphan')
    cart_items = db.relationship('Cart', backref='product', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', cascade='all, delete-orphan')


class Order(db.Model):
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
    order_status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='order', cascade='all, delete-orphan')


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    unit_price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, server_default=db.func.now())
    
    __table_args__ = (db.UniqueConstraint('customer_id', 'product_id', name='unique_cart_item'),)


# ============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================================

def generate_order_number():
    """Генерирует уникальный номер заказа"""
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"


def serialize_product(product):
    """Сериализует объект Product в JSON"""
    return {
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
            'rating': product.seller.rating
        }
    }


# ============================================================================
# API МАРШРУТЫ - АУТЕНТИФИКАЦИЯ
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    try:
        data = request.get_json()
        
        # Проверка обязательных полей
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email и пароль обязательны'}), 400
        
        # Проверка существования пользователя
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Пользователь с этим email уже существует'}), 400
        
        # Создание пользователя
        user = User(
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone=data.get('phone', ''),
            user_type=data.get('user_type', 'customer')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.flush()
        
        # Создание профиля в зависимости от типа пользователя
        if user.user_type == 'seller':
            seller = Seller(
                user_id=user.id,
                shop_name=data.get('shop_name', 'Мой магазин'),
                shop_description=data.get('shop_description', ''),
                shop_address=data.get('shop_address', ''),
                shop_phone=data.get('phone', '')
            )
            db.session.add(seller)
        else:
            customer = Customer(user_id=user.id)
            db.session.add(customer)
        
        db.session.commit()
        
        # Создание JWT токена
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'user_type': user.user_type
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Вход пользователя"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'success': False, 'error': 'Email и пароль обязательны'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'success': False, 'error': 'Неверный email или пароль'}), 401
        
        if not user.is_active:
            return jsonify({'success': False, 'error': 'Аккаунт деактивирован'}), 403
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'user_type': user.user_type
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API МАРШРУТЫ - ТОВАРЫ
# ============================================================================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Получить все товары с фильтрацией"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        occasion = request.args.get('occasion', None)
        size = request.args.get('size', None)
        min_price = request.args.get('min_price', 0, type=float)
        max_price = request.args.get('max_price', float('inf'), type=float)
        
        query = Product.query.filter(Product.is_in_stock == True)
        
        if occasion:
            query = query.filter(Product.occasion == occasion)
        if size:
            query = query.filter(Product.size == size)
        
        query = query.filter(
            Product.price >= min_price,
            Product.price <= max_price
        )
        
        products = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [serialize_product(p) for p in products.items],
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
    """Получить товар по ID"""
    try:
        product = Product.query.get_or_404(product_id)
        return jsonify({
            'success': True,
            'data': serialize_product(product)
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 404


@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    """Создать новый товар (только продавец)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'seller':
            return jsonify({'success': False, 'error': 'Только продавцы могут создавать товары'}), 403
        
        seller = Seller.query.filter_by(user_id=user_id).first()
        data = request.get_json()
        
        product = Product(
            seller_id=seller.id,
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            composition=data.get('composition'),
            occasion=data.get('occasion'),
            size=data.get('size', 'medium'),
            stock_quantity=data.get('stock_quantity', 0),
            is_in_stock=data.get('stock_quantity', 0) > 0,
            image_url=data.get('image_url')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': serialize_product(product)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Обновить товар"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'seller':
            return jsonify({'success': False, 'error': 'Только продавцы могут обновлять товары'}), 403
        
        product = Product.query.get_or_404(product_id)
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if product.seller_id != seller.id:
            return jsonify({'success': False, 'error': 'Вы не можете обновлять чужие товары'}), 403
        
        data = request.get_json()
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.composition = data.get('composition', product.composition)
        product.occasion = data.get('occasion', product.occasion)
        product.size = data.get('size', product.size)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.is_in_stock = product.stock_quantity > 0
        product.image_url = data.get('image_url', product.image_url)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': serialize_product(product)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Удалить товар"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user or user.user_type != 'seller':
            return jsonify({'success': False, 'error': 'Только продавцы могут удалять товары'}), 403
        
        product = Product.query.get_or_404(product_id)
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if product.seller_id != seller.id:
            return jsonify({'success': False, 'error': 'Вы не можете удалять чужие товары'}), 403
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Товар удален'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API МАРШРУТЫ - ЗАКАЗЫ
# ============================================================================

@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    """Создать новый заказ"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        customer = Customer.query.filter_by(user_id=user_id).first()
        
        if not customer:
            return jsonify({'success': False, 'error': 'Только покупатели могут создавать заказы'}), 403
        
        data = request.get_json()
        items = data.get('items', [])
        
        if not items:
            return jsonify({'success': False, 'error': 'Заказ должен содержать товары'}), 400
        
        # Получение первого товара для определения продавца
        first_product = Product.query.get(items[0]['id'])
        
        total_amount = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
        total_amount += 50  # Доставка
        
        order = Order(
            customer_id=customer.id,
            seller_id=first_product.seller_id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            delivery_address=data.get('delivery_address'),
            delivery_date=datetime.strptime(data.get('delivery_date'), '%Y-%m-%d').date(),
            delivery_time=data.get('delivery_time'),
            personal_message=data.get('personal_message'),
            payment_method=data.get('payment_method', 'cash_on_delivery')
        )
        
        db.session.add(order)
        db.session.flush()
        
        # Добавление товаров в заказ
        for item in items:
            product = Product.query.get(item['id'])
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.get('quantity', 1),
                unit_price=product.price,
                subtotal=product.price * item.get('quantity', 1)
            )
            db.session.add(order_item)
            
            # Уменьшение количества товара
            product.stock_quantity -= item.get('quantity', 1)
            if product.stock_quantity <= 0:
                product.is_in_stock = False
        
        # Обновление статистики покупателя
        customer.total_orders += 1
        customer.total_spent += total_amount
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_number': order.order_number,
            'order_id': order.id,
            'total_amount': order.total_amount
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Получить заказы текущего пользователя"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.user_type == 'customer':
            customer = Customer.query.filter_by(user_id=user_id).first()
            orders = Order.query.filter_by(customer_id=customer.id).all()
        elif user.user_type == 'seller':
            seller = Seller.query.filter_by(user_id=user_id).first()
            orders = Order.query.filter_by(seller_id=seller.id).all()
        else:
            return jsonify({'success': False, 'error': 'Неизвестный тип пользователя'}), 400
        
        return jsonify({
            'success': True,
            'data': [{
                'id': order.id,
                'order_number': order.order_number,
                'total_amount': order.total_amount,
                'delivery_address': order.delivery_address,
                'delivery_date': order.delivery_date.isoformat(),
                'order_status': order.order_status,
                'created_at': order.created_at.isoformat()
            } for order in orders]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Обновить статус заказа"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if user.user_type != 'seller':
            return jsonify({'success': False, 'error': 'Только продавцы могут обновлять статус'}), 403
        
        order = Order.query.get_or_404(order_id)
        seller = Seller.query.filter_by(user_id=user_id).first()
        
        if order.seller_id != seller.id:
            return jsonify({'success': False, 'error': 'Вы не можете обновлять чужие заказы'}), 403
        
        data = request.get_json()
        order.order_status = data.get('status')
        db.session.commit()
        
        return jsonify({
            'success': True,
            'order_status': order.order_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API МАРШРУТЫ - ОТЗЫВЫ
# ============================================================================

@app.route('/api/reviews', methods=['POST'])
@jwt_required()
def create_review():
    """Создать отзыв"""
    try:
        user_id = get_jwt_identity()
        customer = Customer.query.filter_by(user_id=user_id).first()
        
        data = request.get_json()
        
        review = Review(
            order_id=data.get('order_id'),
            customer_id=customer.id,
            product_id=data.get('product_id'),
            seller_id=data.get('seller_id'),
            rating=data.get('rating'),
            review_text=data.get('review_text')
        )
        
        db.session.add(review)
        
        # Обновление рейтинга товара
        product = Product.query.get(data.get('product_id'))
        reviews = Review.query.filter_by(product_id=product.id).all()
        avg_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
        product.rating = avg_rating
        product.review_count = len(reviews)
        
        db.session.commit()
        
        return jsonify({'success': True, 'review_id': review.id}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """Получить отзывы товара"""
    try:
        reviews = Review.query.filter_by(product_id=product_id).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': r.id,
                'rating': r.rating,
                'review_text': r.review_text,
                'customer_name': r.customer.user.first_name,
                'created_at': r.created_at.isoformat()
            } for r in reviews]
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============================================================================
# API МАРШРУТЫ - ЗДОРОВЬЕ
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Проверка здоровья приложения"""
    return jsonify({
        'status': 'ok',
        'message': 'Lumme API is running',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200


# ============================================================================
# ОБРАБОТЧИКИ ОШИБОК
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'success': False, 'error': 'Unauthorized'}), 401


# ============================================================================
# ИНИЦИАЛИЗАЦИЯ
# ============================================================================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ База данных инициализирована")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
