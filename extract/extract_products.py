from utils import fetch_data, save_json


def main():
    products = fetch_data("/products")
    save_json(products, "products.json")


if __name__ == "__main__":
    main()