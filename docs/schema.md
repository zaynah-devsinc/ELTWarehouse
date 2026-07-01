# Schema Documentation

## Project

E-Commerce ELT Data Warehouse

## Data Source

API: DummyJSON

Base URL:

https://dummyjson.com

The project currently uses the following endpoints:

- GET /products
- GET /users
- GET /carts

---

# Products

## Endpoint

GET /products

## Description

Contains information about products available in the store.

## Fields Selected for Analysis

| Field | Type | Notes |
|--------|------|-------|
| id | Integer | Product ID |
| title | String | Product name |
| description | String | Product description |
| category | String | Product category |
| price | Decimal | Product price |
| discountPercentage | Decimal | Product discount |
| rating | Decimal | Customer rating |
| stock | Integer | Available inventory |
| brand | String | Product brand |
| sku | String | Stock Keeping Unit (SKU) |

## Fields Ignored

- images
- thumbnail
- reviews
- dimensions
- warrantyInformation
- shippingInformation
- availabilityStatus
- tags
- minimumOrderQuantity
- meta

---

# Users

## Endpoint

GET /users

## Description

Contains customer information.

## Fields Selected for Analysis

| Field | Type | Notes |
|--------|------|-------|
| id | Integer | Customer ID |
| firstName | String | First name |
| lastName | String | Last name |
| email | String | Email address |
| phone | String | Phone number |
| age | Integer | Customer age |
| gender | String | Customer gender |
| birthDate | Date | Date of birth |
| address.city | String | Customer city |
| address.state | String | Customer state |
| address.country | String | Customer country |

## Fields Ignored

- password
- image
- crypto
- bank
- company
- bloodGroup
- hair
- eyeColor
- height
- weight
- ip
- macAddress
- university
- ein
- ssn
- userAgent

---

# Carts

## Endpoint

GET /carts

## Description

Contains shopping cart information. Each cart belongs to one user and contains one or more products.

## Cart Fields Selected for Analysis

| Field | Type | Notes |
|--------|------|-------|
| id | Integer | Cart ID |
| userId | Integer | Customer ID |
| total | Decimal | Cart total |
| discountedTotal | Decimal | Total after discounts |
| totalProducts | Integer | Number of unique products |
| totalQuantity | Integer | Total quantity of items |

## Product Fields Inside Cart

| Field | Type | Notes |
|--------|------|-------|
| id | Integer | Product ID |
| title | String | Product name |
| price | Decimal | Product price |
| quantity | Integer | Quantity purchased |
| total | Decimal | Total price before discount |
| discountPercentage | Decimal | Product discount |
| discountedTotal | Decimal | Total after discount |

## Fields Ignored

- thumbnail
