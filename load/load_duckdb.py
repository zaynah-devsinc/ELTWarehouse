import duckdb
import pandas as pd

connection = duckdb.connect("database/ecommerce.duckdb")

# Enable S3 support
connection.execute("INSTALL httpfs;")
connection.execute("LOAD httpfs;")

# AWS Credentials
connection.execute("SET s3_region='eu-north-1';")
connection.execute("SET s3_access_key_id='AKIA5F2BI4KZEINSJUHH';")
connection.execute("SET s3_secret_access_key='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';")


def load_json_from_s3(filename, key):
    """
    Read a JSON file directly from S3 and return a DataFrame.
    """

    df = connection.execute(f"""
        SELECT *
        FROM read_json_auto(
            's3://elt-warehouse-raw-zaynah/{filename}'
        )
    """).df()

    return pd.DataFrame(list(df[key][0]))


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

    products_df = load_json_from_s3(
        "products.json",
        "products"
    )

    users_df = load_json_from_s3(
        "users.json",
        "users"
    )

    carts_df = load_json_from_s3(
        "carts.json",
        "carts"
    )

    load_table(products_df, "raw_products")
    load_table(users_df, "raw_users")
    load_table(carts_df, "raw_carts")

    connection.close()


if __name__ == "__main__":
    main()