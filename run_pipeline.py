import subprocess

print("=" * 60)
print("Starting ELT Pipeline")
print("=" * 60)

print("\n[1/6] Extracting Products...")
subprocess.run(["python", "extract/extract_products.py"], check=True)

print("\n[2/6] Extracting Users...")
subprocess.run(["python", "extract/extract_users.py"], check=True)

print("\n[3/6] Extracting Carts...")
subprocess.run(["python", "extract/extract_carts.py"], check=True)

print("\n[4/6] Loading data into DuckDB...")
subprocess.run(["python", "load/load_duckdb.py"], check=True)
print("\n[5/6] Running dbt models...")
subprocess.run(
    ["dbt", "run"],
    cwd="ecommerce_dbt",
    check=True
)

print("\n[6/6] Running dbt tests...")
subprocess.run(
    ["dbt", "test"],
    cwd="ecommerce_dbt",
    check=True
)

print("\nELT Pipeline completed successfully!")