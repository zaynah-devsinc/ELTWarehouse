import json

import duckdb
import pandas as pd

connection = duckdb.connect("database/ecommerce.duckdb")



def load_json(file_path, key):
    """
    Read a JSON file and return a DataFrame.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return pd.DataFrame(data[key])


def load_table(df, table_name):
    """
    Load a DataFrame into DuckDB.
    """
    connection.execute(f"""
    CREATE OR REPLACE TABLE {table_name} AS
    SELECT * FROM df
    """)

    rows = connection.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    ).fetchone()[0]

    print(f"{table_name}: {rows} rows loaded")


def main():

    products_df = load_json(
        "data/raw/products.json",
        "products"
    )

    users_df = load_json(
        "data/raw/users.json",
        "users"
    )

    carts_df = load_json(
        "data/raw/carts.json",
        "carts"
    )

    load_table(products_df, "raw_products")
    load_table(users_df, "raw_users")
    load_table(carts_df, "raw_carts")
if __name__ == "__main__":
    main()