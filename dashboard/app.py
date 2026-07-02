import streamlit as st
import duckdb
import plotly.express as px

# 1. Page Configuration
st.set_page_config(
    page_title="E-Commerce ELT Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Connection & Data Fetching
@st.cache_resource
def get_connection():
    return duckdb.connect("database/ecommerce.duckdb")

conn = get_connection()

# Fetch dataframes
sales = conn.sql("SELECT * FROM sales_summary").df()
category = conn.sql("SELECT * FROM category_sales ORDER BY revenue DESC").df()  # Sorted for better visuals
customers = conn.sql("SELECT * FROM customer_summary ORDER BY lifetime_value DESC LIMIT 10").df()
products = conn.sql("SELECT * FROM stg_products ORDER BY product_id").df()

# 3. Sidebar - Clean Architecture Overview
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/analytics.png", width=80)
    st.title("Data Pipeline")
    st.caption("Technical Architecture & Source")
    
    st.markdown("---")
    
    # Modernized pipeline display using status/info widgets
    st.markdown("### 🏗️ ELT Flow")
    st.code("""
DummyJSON API
     ↓  [Python Extract]
Amazon S3 (Raw Layer)
     ↓  [DuckDB Ingest]
dbt Transformations
     ↓  [Semantic Layer]
Streamlit UI
    """, language="text")
    
    st.markdown("---")
    st.info("💡 **Tech Stack:**\nPython, S3, DuckDB, dbt, Streamlit")

# 4. Header Section
st.title("🛒 E-Commerce ELT Dashboard")
st.markdown("Business metrics generated dynamically from the production ELT pipeline.")
st.markdown("---")

# 5. Executive KPIs (Top Level Metrics)
# Wrapped in a container for visual structure
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${sales['total_revenue'][0]:,.2f}",
            
        )
    with col2:
        st.metric(
            label="Total Orders",
            value=f"{int(sales['total_orders'][0]):,}"
        )
    with col3:
        st.metric(
            label="Average Order Value (AOV)",
            value=f"${sales['average_order_value'][0]:,.2f}"
        )
    with col4:
        st.metric(
            label="Total Items Sold",
            value=f"{int(sales['total_items_sold'][0]):,}"
        )

st.markdown("<br>", unsafe_allow_html=True)

# 6. Tabbed View for Clean Layout Presentation
tab_overview, tab_customers, tab_products = st.tabs([
    "📊 Revenue Analysis", 
    "👥 Top Customers", 
    "📦 Product Inventory"
])

# --- TAB 1: OVERVIEW & CHART ---
with tab_overview:
    st.subheader("Revenue Distribution by Category")
    
    # Cleaned up Plotly Bar Chart
    fig = px.bar(
        category,
        x="category",
        y="revenue",
        color="revenue", # Gradient coloring looks more professional than categorical coloring
        color_continuous_scale="Blues",
        text="revenue",
        labels={"category": "Product Category", "revenue": "Revenue ($)"}
    )
    
    fig.update_layout(
        template="plotly_white", # Clean presentation theme
        coloraxis_showscale=False,
        xaxis_tickangle=-30,
        margin=dict(l=20, r=20, t=20, b=40),
        height=500
    )
    
    fig.update_traces(
        texttemplate="$%{text:,.2f}", 
        textposition="outside"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: CUSTOMERS ---
with tab_customers:
    st.subheader("Top 10 High-Value Customers")
    st.markdown("Identified by total lifetime value (LTV) generated via the pipeline.")
    
    # Using column_config to professionally format the dataframe columns
    st.dataframe(
        customers,
        use_container_width=True,
        hide_index=True,
        column_config={
            "customer_id": st.column_config.NumberColumn("ID", format="%d"),
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "total_orders": st.column_config.NumberColumn("Total Orders", format="%d"),
            "lifetime_value": st.column_config.NumberColumn("Lifetime Value (LTV)", format="$%.2f"),
            "average_order_value": st.column_config.NumberColumn("AOV", format="$%.2f")
        }
    )

# --- TAB 3: PRODUCTS & SEARCH ---
with tab_products:
    st.subheader("Inventory & Catalog Lookup")
    
    # Search bar optimized into columns
    search_col, _ = st.columns([1, 2])
    with search_col:
        search = st.text_input("🔍 Filter catalog by product name", placeholder="Type a product...")

    filtered_products = products[
        products["title"].str.contains(search, case=False, na=False)
    ]
    
    # Selected clean view of columns with formatted prices and progress bars for stock
    st.dataframe(
        filtered_products[[
            "product_id", "title", "category", "brand", "price", "stock"
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "product_id": st.column_config.NumberColumn("Product ID", format="%d"),
            "title": "Product Title",
            "category": "Category",
            "brand": "Brand",
            "price": st.column_config.NumberColumn("Unit Price", format="$%.2f"),
            "stock": st.column_config.ProgressColumn("Stock Level", min_value=0, max_value=150, format="%d units")
        }
    )