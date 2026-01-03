/**
 * Конфигурация API для Lumme маркетплейса
 */

// API базовый URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://lumme-production.up.railway.app/api';

// Класс для работы с API
class LummeAPI {
    constructor(baseURL = API_BASE_URL) {
        this.baseURL = baseURL;
        this.token = localStorage.getItem('token');
    }

    // Установка токена
    setToken(token) {
        this.token = token;
        localStorage.setItem('token', token);
    }

    // Получение токена
    getToken() {
        return this.token;
    }

    // Выход (удаление токена)
    logout() {
        this.token = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        localStorage.removeItem('cart');
    }

    // Базовый метод для запросов
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'API Error');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // ========== АУТЕНТИФИКАЦИЯ ==========

    async register(userData) {
        return this.request('/auth/register', {
            method: 'POST',
            body: JSON.stringify(userData)
        });
    }

    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ email, password })
        });
    }

    // ========== ТОВАРЫ ==========

    async getProducts(filters = {}) {
        const params = new URLSearchParams();
        
        if (filters.page) params.append('page', filters.page);
        if (filters.per_page) params.append('per_page', filters.per_page);
        if (filters.occasion) params.append('occasion', filters.occasion);
        if (filters.size) params.append('size', filters.size);
        if (filters.min_price) params.append('min_price', filters.min_price);
        if (filters.max_price) params.append('max_price', filters.max_price);

        const query = params.toString();
        const endpoint = `/products${query ? '?' + query : ''}`;

        return this.request(endpoint);
    }

    async getProduct(productId) {
        return this.request(`/products/${productId}`);
    }

    async createProduct(productData) {
        return this.request('/products', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    }

    async updateProduct(productId, productData) {
        return this.request(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(productData)
        });
    }

    async deleteProduct(productId) {
        return this.request(`/products/${productId}`, {
            method: 'DELETE'
        });
    }

    // ========== ЗАКАЗЫ ==========

    async createOrder(orderData) {
        return this.request('/orders', {
            method: 'POST',
            body: JSON.stringify(orderData)
        });
    }

    async getOrders() {
        return this.request('/orders');
    }

    async updateOrderStatus(orderId, status) {
        return this.request(`/orders/${orderId}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
    }

    // ========== ОТЗЫВЫ ==========

    async createReview(reviewData) {
        return this.request('/reviews', {
            method: 'POST',
            body: JSON.stringify(reviewData)
        });
    }

    async getProductReviews(productId) {
        return this.request(`/products/${productId}/reviews`);
    }

    // ========== ЗДОРОВЬЕ ==========

    async healthCheck() {
        return this.request('/health');
    }
}

// Создание глобального экземпляра API
const api = new LummeAPI();

// Экспорт для использования в других файлах
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LummeAPI, api };
}
