# Zest Store - Advanced E-commerce Backend API

## Overview

Zest Store is a powerful e-commerce backend API built with Django Ninja and GraphQL, optimized for the Bangladesh market. The API provides comprehensive features for authentication, product management, checkout, payments, and more, utilizing PostgreSQL, MongoDB, and Redis for efficient data handling.

## Core Technologies

- **Framework:** Django Ninja with GraphQL support
- **Databases:** PostgreSQL (primary), MongoDB (flexible data)
- **Caching:** Redis
- **Storage:** Vercel Blob Storage
- **Deployment:** Vercel and Github with CI/CD pipeline
- **Monitoring:** Sentry, LogRocket

## Key Features

### Authentication & Security

- JWT-based authentication (register, login, logout)
- OAuth integration (Google, Facebook, Apple)
- Password reset via email verification
- API key & secret authentication
- Role-based access control
- Rate limiting and IP whitelisting (Bangladesh-only access)

### Product Management

- Nested category structure
- Product variations (size, color)
- Multiple product images via Vercel Blob
- Inventory tracking with alerts
- AI-powered recommendations
- SEO-friendly metadata
- Rich text product descriptions

### Orders & Checkout

- Shopping cart management
- Multiple payment gateways:
  - bKash
  - Nagad
  - Rocket
  - Upay
- Order tracking
- Discount system
- Guest checkout
- One-click purchase
- Cash on Delivery (COD)

### Localization

- Primary currency: BDT (Bangladeshi Taka)
- Bilingual support (English & Bangla)

### Customer Engagement

- Email notifications
- Push notifications
- Live chat support API
- AI chatbot integration
- Loyalty & rewards program
- Affiliate/referral system

### Admin Features

- Comprehensive Django admin panel
- Site customization options
- Analytics dashboard
- User activity monitoring
- Multi-vendor support
- Role-based dashboards

## API Workflows

### Authentication Flow

1. User registration (email/password or OAuth)
2. Login → JWT token issued
3. API requests with JWT + API key/secret
4. Password reset process
5. Token invalidation on logout

### Product Management Flow

1. Category creation (nested structure)
2. Product creation:
   - Basic details (title, description, price)
   - Image upload to Vercel Blob
   - Variation configuration
   - Category/tag assignment
3. Inventory management
4. Product recommendations

### Checkout Flow

1. Cart management
2. Shipping details
3. Payment processing
4. Order confirmation
5. Status notifications

### Admin Operations

1. User/role management
2. Order processing
3. Inventory control
4. Analytics review
5. Site customization
6. Vendor management

## Security Measures

- API key & secret required for all requests
- JWT-based user authentication
- Role-based access control
- Request rate limiting
- Bangladesh IP whitelist
- Fraud detection system

## Deployment Architecture

- API hosted on Vercel
- Database cluster configuration
- CDN for static assets
- Automated deployment pipeline
- Error tracking & logging
- Performance monitoring

## Database Schema

### PostgreSQL Schema

#### User Management
```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    full_name VARCHAR(255),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    is_staff BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Profiles
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    avatar_url VARCHAR(255),
    bio TEXT,
    preferences JSONB,
    last_login TIMESTAMP
);

-- Addresses
CREATE TABLE addresses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    is_default BOOLEAN DEFAULT false
);
```

#### Product Management
```sql
-- Categories
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name VARCHAR(100),
    slug VARCHAR(100) UNIQUE,
    parent_id UUID REFERENCES categories(id),
    description TEXT,
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true
);

-- Products
CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    slug VARCHAR(255) UNIQUE,
    description TEXT,
    price DECIMAL(10,2),
    compare_price DECIMAL(10,2),
    cost_price DECIMAL(10,2),
    sku VARCHAR(100) UNIQUE,
    quantity INTEGER,
    category_id UUID REFERENCES categories(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Product Images
CREATE TABLE product_images (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    image_url VARCHAR(255),
    alt_text VARCHAR(255),
    is_primary BOOLEAN DEFAULT false
);

-- Product Variations
CREATE TABLE product_variations (
    id UUID PRIMARY KEY,
    product_id UUID REFERENCES products(id),
    variation_type VARCHAR(50),
    variation_value VARCHAR(50),
    price_adjustment DECIMAL(10,2),
    quantity INTEGER
);
```

#### Order Management
```sql
-- Orders
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    status VARCHAR(50),
    total_amount DECIMAL(10,2),
    shipping_address_id UUID REFERENCES addresses(id),
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order Items
CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id),
    product_id UUID REFERENCES products(id),
    variation_id UUID REFERENCES product_variations(id),
    quantity INTEGER,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2)
);

-- Payments
CREATE TABLE payments (
    id UUID PRIMARY KEY,
    order_id UUID REFERENCES orders(id),
    amount DECIMAL(10,2),
    provider VARCHAR(50),
    status VARCHAR(50),
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### MongoDB Collections

```javascript
// Product Reviews
{
    _id: ObjectId,
    product_id: UUID,
    user_id: UUID,
    rating: Number,
    review_text: String,
    images: Array,
    helpful_votes: Number,
    created_at: DateTime
}

// User Activity
{
    _id: ObjectId,
    user_id: UUID,
    activity_type: String,
    details: Object,
    timestamp: DateTime
}

// Product Analytics
{
    _id: ObjectId,
    product_id: UUID,
    views: Number,
    purchases: Number,
    cart_adds: Number,
    last_updated: DateTime
}
```

### Redis Data Structure

```redis
# Cart Data
cart:{user_id} -> Hash
    product_id -> quantity

# Session Data
session:{session_id} -> Hash
    user_id
    expires
    data

# Cache
product:{product_id}:details -> Hash
category:{category_id}:products -> Set
user:{user_id}:recent_views -> List
```

## Project Structure

```
zest_store/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── apps/
│   ├── core/
│   │   ├── management/
│   │   ├── migrations/
│   │   └── models/
│   ├── users/
│   │   ├── api/
│   │   ├── services/
│   │   └── tests/
│   ├── products/
│   │   ├── api/
│   │   ├── services/
│   │   └── tests/
│   ├── orders/
│   │   ├── api/
│   │   ├── services/
│   │   └── tests/
│   └── payments/
│       ├── api/
│       ├── services/
│       └── tests/
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── utils/
│   ├── helpers/
│   ├── middleware/
│   └── validators/
├── services/
│   ├── email/
│   ├── storage/
│   └── payment_gateways/
├── tests/
│   ├── integration/
│   └── unit/
├── docs/
│   ├── API-REFERENCE.md
│   └── CONTEXT.md
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

For detailed API documentation and integration guides, please refer to our [API Reference](./API-REFERENCE.md).