import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce ELT Dashboard",
    page_icon="🛒",
    layout="wide"
)

#duckdb connection

conn = duckdb.connect("database/ecommerce.duckdb")

#loading DUCKDB tables -> pandas Dataframes

sales = conn.sql("""
SELECT *
FROM sales_summary
""").df()

category = conn.sql("""
SELECT *
FROM category_sales
""").df()

customers = conn.sql("""
SELECT *
FROM customer_summary
ORDER BY lifetime_value DESC
LIMIT 10
""").df()

products = conn.sql("""
SELECT *
FROM stg_products
ORDER BY product_id
""").df()

#random sidebar

st.sidebar.title("Project Overview")

st.sidebar.markdown("""
### E-Commerce ELT Pipeline

DummyJSON API

↓

Python Extraction

↓

Amazon S3 (Raw Layer)

↓

DuckDB

↓

dbt Transformations

↓

Streamlit Dashboard
""")

#title
st.title("E-Commerce ELT Dashboard")

st.markdown("Business metrics generated from the ELT pipeline.")

#KPIs

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${sales['total_revenue'][0]:,.2f}"
)

col2.metric(
    "Total Orders",
    int(sales["total_orders"][0])
)

col3.metric(
    "Average Order Value",
    f"${sales['average_order_value'][0]:,.2f}"
)

col4.metric(
    "Items Sold",
    int(sales["total_items_sold"][0])
)

#category revenue

st.divider()

st.subheader("Revenue by Category")

fig = px.bar(
    category,
    x="category",
    y="revenue",
    color="category",
    text="revenue"
)

fig.update_layout(
    showlegend=False,
    xaxis_title="Category",
    yaxis_title="Revenue"
)

fig.update_traces(texttemplate="$%{text:,.2f}")

st.plotly_chart(fig, use_container_width=True)

#TOP Customers

st.divider()

st.subheader("Top Customers")

customers["lifetime_value"] = customers["lifetime_value"].round(2)
customers["average_order_value"] = customers["average_order_value"].round(2)

st.dataframe(
    customers,
    use_container_width=True,
    hide_index=True
)

#All Prods 

st.divider()

st.subheader("Products")

search = st.text_input("Search Product")

filtered_products = products[
    products["title"].str.contains(
        search,
        case=False,
        na=False
    )
]

st.dataframe(
    filtered_products[
        [
            "product_id",
            "title",
            "category",
            "brand",
            "price",
            "stock"
        ]
    ],
    use_container_width=True,
    hide_index=True
)