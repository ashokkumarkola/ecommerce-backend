# Production-Grade Ecommerce Database Schema

## Overview

This document defines the core database schema for a modern production-grade ecommerce backend.

Design goals:

- scalability
- maintainability
- normalization
- transactional consistency
- clean relationships
- production readiness
- extensibility

Database:

- PostgreSQL

Architecture Style:

- Modular Monolith
- Relational Database Design
- ACID Transaction Support

---

# Core Modules

```text
Users
Authentication
Catalog
Inventory
Cart
Orders
Payments
Reviews
Wishlists
Discounts
Shipping
RBAC
Audit Logs
```

---

# 1. USERS

## Table: users

### Purpose

Stores authentication and account information.

| Column        | Type      | Constraints      | Description               |
| ------------- | --------- | ---------------- | ------------------------- |
| id            | UUID      | PK               | Unique user ID            |
| email         | VARCHAR   | UNIQUE, NOT NULL | User email                |
| password_hash | TEXT      | NOT NULL         | Hashed password           |
| phone         | VARCHAR   | UNIQUE           | Phone number              |
| is_active     | BOOLEAN   | DEFAULT TRUE     | Active account status     |
| is_verified   | BOOLEAN   | DEFAULT FALSE    | Email verification status |
| created_at    | TIMESTAMP | NOT NULL         | Creation timestamp        |
| updated_at    | TIMESTAMP | NOT NULL         | Last update timestamp     |

### Indexes

```text
email
phone
```

### Features

- authentication
- account activation
- email verification
- login management

---

# 2. USER PROFILES

## Table: user_profiles

### Purpose

Stores optional profile information.

| Column        | Type    | Constraints        | Description    |
| ------------- | ------- | ------------------ | -------------- |
| user_id       | UUID    | PK, FK -> users.id | User reference |
| first_name    | VARCHAR |                    | First name     |
| last_name     | VARCHAR |                    | Last name      |
| date_of_birth | DATE    |                    | Date of birth  |
| gender        | VARCHAR |                    | Gender         |
| avatar_url    | TEXT    |                    | Profile image  |

### Relationship

```text
users -> user_profiles
One-to-One
```

### Features

- profile management
- avatar support
- extensible user metadata

---

# 3. ADDRESSES

## Table: addresses

### Purpose

Stores user shipping and billing addresses.

| Column         | Type      | Constraints    | Description       |
| -------------- | --------- | -------------- | ----------------- |
| id             | UUID      | PK             | Address ID        |
| user_id        | UUID      | FK -> users.id | Owner user        |
| full_name      | VARCHAR   | NOT NULL       | Receiver name     |
| phone          | VARCHAR   | NOT NULL       | Receiver phone    |
| address_line_1 | TEXT      | NOT NULL       | Primary address   |
| address_line_2 | TEXT      |                | Secondary address |
| city           | VARCHAR   | NOT NULL       | City              |
| state          | VARCHAR   | NOT NULL       | State             |
| country        | VARCHAR   | NOT NULL       | Country           |
| postal_code    | VARCHAR   | NOT NULL       | Postal code       |
| is_default     | BOOLEAN   | DEFAULT FALSE  | Default address   |
| created_at     | TIMESTAMP | NOT NULL       | Created timestamp |

### Relationship

```text
users -> addresses
One-to-Many
```

### Features

- multiple addresses
- shipping support
- billing support
- default address selection

---

# 4. ROLES

## Table: roles

### Purpose

Stores RBAC roles.

| Column | Type    | Constraints | Description |
| ------ | ------- | ----------- | ----------- |
| id     | UUID    | PK          | Role ID     |
| name   | VARCHAR | UNIQUE      | Role name   |

### Example Roles

```text
Admin
Customer
Seller
Support
Warehouse Manager
```

---

# 5. USER ROLES

## Table: user_roles

### Purpose

Maps users to roles.

| Column  | Type | Constraints    | Description    |
| ------- | ---- | -------------- | -------------- |
| id      | UUID | PK             | Record ID      |
| user_id | UUID | FK -> users.id | User reference |
| role_id | UUID | FK -> roles.id | Role reference |

### Features

- RBAC
- multiple roles per user
- admin permission system

---

# 6. CATEGORIES

## Table: categories

### Purpose

Stores hierarchical product categories.

| Column             | Type    | Constraints         | Description     |
| ------------------ | ------- | ------------------- | --------------- |
| id                 | UUID    | PK                  | Category ID     |
| parent_category_id | UUID    | FK -> categories.id | Parent category |
| name               | VARCHAR | NOT NULL            | Category name   |
| slug               | VARCHAR | UNIQUE              | SEO slug        |
| description        | TEXT    |                     | Description     |

### Relationship

```text
Self-referencing hierarchy
```

### Features

- category nesting
- SEO support
- product grouping

---

# 7. PRODUCTS

## Table: products

### Purpose

Stores main product information.

| Column      | Type      | Constraints         | Description         |
| ----------- | --------- | ------------------- | ------------------- |
| id          | UUID      | PK                  | Product ID          |
| category_id | UUID      | FK -> categories.id | Product category    |
| seller_id   | UUID      | FK -> users.id      | Product seller      |
| title       | VARCHAR   | NOT NULL            | Product title       |
| slug        | VARCHAR   | UNIQUE              | SEO slug            |
| description | TEXT      |                     | Product description |
| brand       | VARCHAR   |                     | Brand               |
| status      | VARCHAR   | NOT NULL            | Product status      |
| created_at  | TIMESTAMP | NOT NULL            | Created timestamp   |
| updated_at  | TIMESTAMP | NOT NULL            | Updated timestamp   |

### Indexes

```text
title
slug
category_id
seller_id
```

### Features

- SEO-friendly products
- seller-based products
- product lifecycle management

---

# 8. PRODUCT VARIANTS

## Table: product_variants

### Purpose

Stores product variations.

| Column        | Type    | Constraints       | Description           |
| ------------- | ------- | ----------------- | --------------------- |
| id            | UUID    | PK                | Variant ID            |
| product_id    | UUID    | FK -> products.id | Parent product        |
| sku           | VARCHAR | UNIQUE            | Stock keeping unit    |
| price         | NUMERIC | CHECK >= 0        | Selling price         |
| compare_price | NUMERIC | CHECK >= 0        | Original price        |
| weight        | NUMERIC | CHECK >= 0        | Product weight        |
| color         | VARCHAR |                   | Variant color         |
| size          | VARCHAR |                   | Variant size          |
| storage       | VARCHAR |                   | Storage specification |
| is_active     | BOOLEAN | DEFAULT TRUE      | Active status         |

### Relationship

```text
products -> product_variants
One-to-Many
```

### Features

- size variants
- color variants
- SKU management
- flexible pricing

---

# 9. PRODUCT IMAGES

## Table: product_images

### Purpose

Stores product images.

| Column             | Type    | Constraints               | Description       |
| ------------------ | ------- | ------------------------- | ----------------- |
| id                 | UUID    | PK                        | Image ID          |
| product_variant_id | UUID    | FK -> product_variants.id | Variant reference |
| image_url          | TEXT    | NOT NULL                  | Image URL         |
| sort_order         | INTEGER | DEFAULT 0                 | Display order     |

### Features

- multiple images
- image sorting
- CDN integration ready

---

# 10. INVENTORY

## Table: inventory

### Purpose

Tracks product stock.

| Column             | Type      | Constraints               | Description       |
| ------------------ | --------- | ------------------------- | ----------------- |
| id                 | UUID      | PK                        | Inventory ID      |
| product_variant_id | UUID      | FK -> product_variants.id | Variant reference |
| quantity_available | INTEGER   | CHECK >= 0                | Available stock   |
| quantity_reserved  | INTEGER   | CHECK >= 0                | Reserved stock    |
| reorder_level      | INTEGER   | CHECK >= 0                | Reorder threshold |
| updated_at         | TIMESTAMP | NOT NULL                  | Last stock update |

### Features

- stock management
- reservation system
- overselling prevention
- low stock alerts

---

# 11. CARTS

## Table: carts

### Purpose

Stores user shopping carts.

| Column     | Type      | Constraints    | Description       |
| ---------- | --------- | -------------- | ----------------- |
| id         | UUID      | PK             | Cart ID           |
| user_id    | UUID      | FK -> users.id | Cart owner        |
| created_at | TIMESTAMP | NOT NULL       | Created timestamp |
| updated_at | TIMESTAMP | NOT NULL       | Updated timestamp |

### Relationship

```text
users -> carts
One-to-One
```

---

# 12. CART ITEMS

## Table: cart_items

### Purpose

Stores products added to cart.

| Column             | Type    | Constraints               | Description     |
| ------------------ | ------- | ------------------------- | --------------- |
| id                 | UUID    | PK                        | Cart item ID    |
| cart_id            | UUID    | FK -> carts.id            | Cart reference  |
| product_variant_id | UUID    | FK -> product_variants.id | Product variant |
| quantity           | INTEGER | CHECK > 0                 | Item quantity   |

### Features

- cart persistence
- quantity tracking
- many-to-many resolution

---

# 13. ORDERS

## Table: orders

### Purpose

Stores order master records.

| Column          | Type      | Constraints        | Description         |
| --------------- | --------- | ------------------ | ------------------- |
| id              | UUID      | PK                 | Order ID            |
| user_id         | UUID      | FK -> users.id     | Customer            |
| address_id      | UUID      | FK -> addresses.id | Shipping address    |
| status          | VARCHAR   | NOT NULL           | Order status        |
| payment_status  | VARCHAR   | NOT NULL           | Payment status      |
| subtotal        | NUMERIC   | CHECK >= 0         | Product subtotal    |
| tax_amount      | NUMERIC   | CHECK >= 0         | Tax amount          |
| shipping_amount | NUMERIC   | CHECK >= 0         | Shipping fee        |
| discount_amount | NUMERIC   | CHECK >= 0         | Discount amount     |
| grand_total     | NUMERIC   | CHECK >= 0         | Final total         |
| placed_at       | TIMESTAMP | NOT NULL           | Order creation time |

### Indexes

```text
user_id
placed_at
status
```

### Features

- transactional order management
- order lifecycle tracking
- financial tracking

---

# 14. ORDER ITEMS

## Table: order_items

### Purpose

Stores purchased product snapshots.

| Column             | Type    | Constraints               | Description            |
| ------------------ | ------- | ------------------------- | ---------------------- |
| id                 | UUID    | PK                        | Order item ID          |
| order_id           | UUID    | FK -> orders.id           | Parent order           |
| product_variant_id | UUID    | FK -> product_variants.id | Purchased variant      |
| product_name       | VARCHAR | NOT NULL                  | Snapshot product title |
| sku                | VARCHAR | NOT NULL                  | Snapshot SKU           |
| price              | NUMERIC | CHECK >= 0                | Snapshot price         |
| quantity           | INTEGER | CHECK > 0                 | Purchased quantity     |
| total              | NUMERIC | CHECK >= 0                | Line total             |

### Features

- historical accuracy
- immutable purchase records
- invoice generation support

---

# 15. PAYMENTS

## Table: payments

### Purpose

Stores payment transaction details.

| Column           | Type      | Constraints     | Description            |
| ---------------- | --------- | --------------- | ---------------------- |
| id               | UUID      | PK              | Payment ID             |
| order_id         | UUID      | FK -> orders.id | Related order          |
| payment_provider | VARCHAR   | NOT NULL        | Payment gateway        |
| transaction_id   | VARCHAR   | UNIQUE          | Gateway transaction ID |
| amount           | NUMERIC   | CHECK >= 0      | Paid amount            |
| currency         | VARCHAR   | NOT NULL        | Currency               |
| status           | VARCHAR   | NOT NULL        | Payment status         |
| paid_at          | TIMESTAMP |                 | Payment timestamp      |

### Features

- payment lifecycle tracking
- refund support
- transaction auditing
- gateway integrations

---

# 16. SHIPMENTS

## Table: shipments

### Purpose

Tracks shipment and delivery information.

| Column            | Type      | Constraints     | Description              |
| ----------------- | --------- | --------------- | ------------------------ |
| id                | UUID      | PK              | Shipment ID              |
| order_id          | UUID      | FK -> orders.id | Related order            |
| tracking_number   | VARCHAR   | UNIQUE          | Shipment tracking number |
| shipping_provider | VARCHAR   | NOT NULL        | Courier provider         |
| status            | VARCHAR   | NOT NULL        | Shipment status          |
| shipped_at        | TIMESTAMP |                 | Shipment timestamp       |
| delivered_at      | TIMESTAMP |                 | Delivery timestamp       |

### Features

- shipment tracking
- courier integration
- delivery lifecycle management

---

# 17. REVIEWS

## Table: reviews

### Purpose

Stores customer reviews and ratings.

| Column     | Type      | Constraints           | Description      |
| ---------- | --------- | --------------------- | ---------------- |
| id         | UUID      | PK                    | Review ID        |
| user_id    | UUID      | FK -> users.id        | Reviewer         |
| product_id | UUID      | FK -> products.id     | Reviewed product |
| rating     | INTEGER   | CHECK BETWEEN 1 AND 5 | Rating score     |
| comment    | TEXT      |                       | Review comment   |
| created_at | TIMESTAMP | NOT NULL              | Review timestamp |

### Constraints

```text
One review per user per product
```

### Features

- ratings system
- customer feedback
- product trust building

---

# 18. WISHLISTS

## Table: wishlists

### Purpose

Stores customer wishlists.

| Column     | Type      | Constraints    | Description       |
| ---------- | --------- | -------------- | ----------------- |
| id         | UUID      | PK             | Wishlist ID       |
| user_id    | UUID      | FK -> users.id | Wishlist owner    |
| created_at | TIMESTAMP | NOT NULL       | Created timestamp |

---

# 19. WISHLIST ITEMS

## Table: wishlist_items

### Purpose

Stores products saved in wishlists.

| Column      | Type | Constraints        | Description        |
| ----------- | ---- | ------------------ | ------------------ |
| id          | UUID | PK                 | Wishlist item ID   |
| wishlist_id | UUID | FK -> wishlists.id | Wishlist reference |
| product_id  | UUID | FK -> products.id  | Saved product      |

### Features

- saved products
- future purchase support
- recommendation systems

---

# 20. DISCOUNTS

## Table: discounts

### Purpose

Stores coupon and promotion rules.

| Column               | Type      | Constraints | Description         |
| -------------------- | --------- | ----------- | ------------------- |
| id                   | UUID      | PK          | Discount ID         |
| code                 | VARCHAR   | UNIQUE      | Coupon code         |
| discount_type        | VARCHAR   | NOT NULL    | Percentage or fixed |
| discount_value       | NUMERIC   | CHECK >= 0  | Discount amount     |
| minimum_order_amount | NUMERIC   | CHECK >= 0  | Minimum cart value  |
| starts_at            | TIMESTAMP | NOT NULL    | Start time          |
| ends_at              | TIMESTAMP | NOT NULL    | Expiry time         |
| usage_limit          | INTEGER   | CHECK >= 0  | Maximum usages      |

### Features

- coupon system
- promotional campaigns
- order discounts

---

# 21. ORDER DISCOUNTS

## Table: order_discounts

### Purpose

Tracks discounts applied to orders.

| Column          | Type    | Constraints        | Description      |
| --------------- | ------- | ------------------ | ---------------- |
| id              | UUID    | PK                 | Record ID        |
| order_id        | UUID    | FK -> orders.id    | Order reference  |
| discount_id     | UUID    | FK -> discounts.id | Applied discount |
| discount_amount | NUMERIC | CHECK >= 0         | Actual discount  |

---

# 22. AUDIT LOGS

## Table: audit_logs

### Purpose

Tracks critical data changes.

| Column      | Type      | Constraints    | Description          |
| ----------- | --------- | -------------- | -------------------- |
| id          | UUID      | PK             | Audit ID             |
| table_name  | VARCHAR   | NOT NULL       | Modified table       |
| record_id   | UUID      | NOT NULL       | Modified record      |
| action_type | VARCHAR   | NOT NULL       | INSERT/UPDATE/DELETE |
| old_data    | JSONB     |                | Previous data        |
| new_data    | JSONB     |                | Updated data         |
| changed_by  | UUID      | FK -> users.id | Actor                |
| changed_at  | TIMESTAMP | NOT NULL       | Change timestamp     |

### Features

- compliance tracking
- admin auditing
- security monitoring
- historical recovery

---

# Relationship Summary

## One-to-One

```text
users -> user_profiles
users -> carts
```

---

## One-to-Many

```text
users -> addresses
users -> orders
categories -> products
products -> product_variants
orders -> order_items
orders -> payments
orders -> shipments
```

---

## Many-to-Many

```text
carts <-> product_variants
wishlists <-> products
```

Resolved Using:

```text
cart_items
wishlist_items
```

---

# Important Constraints

## UNIQUE Constraints

```text
users.email
users.phone
products.slug
product_variants.sku
payments.transaction_id
discounts.code
```

---

## CHECK Constraints

```text
price >= 0
quantity >= 0
rating BETWEEN 1 AND 5
```

---

## FOREIGN KEY Constraints

```text
orders.user_id -> users.id
payments.order_id -> orders.id
inventory.product_variant_id -> product_variants.id
```

---

# Recommended Indexes

```text
users.email
products.slug
products.category_id
orders.user_id
orders.placed_at
payments.transaction_id
inventory.product_variant_id
```

---

# Final Notes

This schema is designed for:

- production-grade ecommerce systems
- scalable backend architecture
- transactional consistency
- modular backend development
- future extensibility

Recommended Stack:

- PostgreSQL
- SQLAlchemy 2.0
- FastAPI
- Redis
- Alembic
