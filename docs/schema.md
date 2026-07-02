# Schema Documentation

## Project Overview

This project is an **E-Commerce ELT Data Warehouse** that uses data from the **DummyJSON API**. The objective is to extract product, customer, and shopping cart data, transform it into a structured format, and load it into a data warehouse for analysis and reporting.

### API Base URL

```text
https://dummyjson.com
```

### API Endpoints Used

* `GET /products`
* `GET /users`
* `GET /carts`

---

# Products

## Endpoint

`GET /products`

## Description

The Products endpoint provides information about all products available in the online store. Only the fields required for analysis are included in the warehouse.

### Fields Used

| Field              | Type    | Description                 |
| ------------------ | ------- | --------------------------- |
| id                 | Integer | Unique product ID           |
| title              | String  | Product name                |
| description        | String  | Product description         |
| category           | String  | Product category            |
| price              | Decimal | Selling price               |
| discountPercentage | Decimal | Product discount percentage |
| rating             | Decimal | Average customer rating     |
| stock              | Integer | Available inventory         |
| brand              | String  | Product brand               |
| sku                | String  | Stock Keeping Unit (SKU)    |

### Fields Excluded

The following fields were available in the API but were not required for this project:

* images
* thumbnail
* reviews
* dimensions
* warrantyInformation
* shippingInformation
* availabilityStatus
* tags
* minimumOrderQuantity
* meta

---

# Users

## Endpoint

`GET /users`

## Description

The Users endpoint contains customer information used for customer analysis and reporting. Only basic customer details were selected.

### Fields Used

| Field           | Type    | Description           |
| --------------- | ------- | --------------------- |
| id              | Integer | Unique customer ID    |
| firstName       | String  | Customer's first name |
| lastName        | String  | Customer's last name  |
| email           | String  | Email address         |
| phone           | String  | Contact number        |
| age             | Integer | Customer age          |
| gender          | String  | Customer gender       |
| birthDate       | Date    | Date of birth         |
| address.city    | String  | Customer city         |
| address.state   | String  | Customer state        |
| address.country | String  | Customer country      |

### Fields Excluded

The following fields were not needed for the data warehouse:

* password
* image
* crypto
* bank
* company
* bloodGroup
* hair
* eyeColor
* height
* weight
* ip
* macAddress
* university
* ein
* ssn
* userAgent

---

# Carts

## Endpoint

`GET /carts`

## Description

The Carts endpoint contains shopping cart information. Each cart belongs to a customer and contains one or more products along with quantity and pricing details.

### Cart Fields Used

| Field           | Type    | Description                       |
| --------------- | ------- | --------------------------------- |
| id              | Integer | Cart ID                           |
| userId          | Integer | Customer ID                       |
| total           | Decimal | Total cart value before discounts |
| discountedTotal | Decimal | Total value after discounts       |
| totalProducts   | Integer | Number of different products      |
| totalQuantity   | Integer | Total quantity of items           |

### Product Fields Used in Each Cart

| Field              | Type    | Description                 |
| ------------------ | ------- | --------------------------- |
| id                 | Integer | Product ID                  |
| title              | String  | Product name                |
| price              | Decimal | Price per item              |
| quantity           | Integer | Quantity purchased          |
| total              | Decimal | Total price before discount |
| discountPercentage | Decimal | Discount percentage         |
| discountedTotal    | Decimal | Total price after discount  |

### Fields Excluded

The following field was not required for analysis:

* thumbnail

---

## Summary

The data warehouse is built using three main datasets:

* **Products** for product-related information
* **Users** for customer details
* **Carts** for purchase and transaction information

Only the fields relevant to reporting and analytics were selected. Unnecessary or sensitive fields were excluded to keep the warehouse simple, efficient, and focused on business analysis.
