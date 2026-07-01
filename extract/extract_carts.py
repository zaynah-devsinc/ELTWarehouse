from utils import fetch_data, save_json


def main():
    carts = fetch_data("/carts")
    save_json(carts, "carts.json")


if __name__ == "__main__":
    main()