from utils import fetch_data, save_json


def main():
    users = fetch_data("/users")
    save_json(users, "users.json")


if __name__ == "__main__":
    main()