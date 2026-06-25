import json
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

PRODUCTS_FILE = DATA_DIR / "products.json"
USERS_FILE = DATA_DIR / "users.json"
PROMOCODES_FILE = DATA_DIR / "promocodes.json"


def ensure_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not PRODUCTS_FILE.exists():
        PRODUCTS_FILE.write_text("[]", encoding="utf-8")

    if not USERS_FILE.exists():
        USERS_FILE.write_text("{}", encoding="utf-8")

    if not PROMOCODES_FILE.exists():
        PROMOCODES_FILE.write_text("{}", encoding="utf-8")


def load_products():
    ensure_files()
    with open(PRODUCTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_products(products):
    ensure_files()
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as file:
        json.dump(products, file, ensure_ascii=False, indent=4)


def load_users():
    ensure_files()
    with open(USERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_users(users):
    ensure_files()
    with open(USERS_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=4)


def load_promocodes():
    ensure_files()
    with open(PROMOCODES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_promocodes(promocodes):
    ensure_files()
    with open(PROMOCODES_FILE, "w", encoding="utf-8") as file:
        json.dump(promocodes, file, ensure_ascii=False, indent=4)


def get_user(user_id: int):
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "purchases": [],
            "language": "ru"
        }
        save_users(users)

    if "language" not in users[user_id]:
        users[user_id]["language"] = "ru"

    if "purchases" not in users[user_id]:
        users[user_id]["purchases"] = []

    if "balance" not in users[user_id]:
        users[user_id]["balance"] = 0

    save_users(users)

    return users[user_id]


def add_balance(user_id: int, amount: int):
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "purchases": [],
            "language": "ru"
        }

    users[user_id]["balance"] += amount
    save_users(users)

    return users[user_id]["balance"]


def remove_balance(user_id: int, amount: int):
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "purchases": [],
            "language": "ru"
        }

    users[user_id]["balance"] -= amount

    if users[user_id]["balance"] < 0:
        users[user_id]["balance"] = 0

    save_users(users)

    return users[user_id]["balance"]


def toggle_language(user_id: int):
    users = load_users()
    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "purchases": [],
            "language": "ru"
        }

    current_language = users[user_id].get("language", "ru")
    new_language = "en" if current_language == "ru" else "ru"

    users[user_id]["language"] = new_language
    save_users(users)

    return new_language


def add_product(category, name, price, description, content, delivery_type="static"):
    products = load_products()

    if delivery_type == "dynamic":
        final_content = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]
    else:
        final_content = content

    product = {
        "id": str(uuid.uuid4())[:8],
        "category": category,
        "name": name,
        "price": int(price),
        "description": description,
        "content": final_content,
        "delivery_type": delivery_type,
        "active": True
    }

    products.append(product)
    save_products(products)

    return product


def delete_product(product_id: str):
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            product["active"] = False
            save_products(products)
            return True

    return False


def get_categories():
    products = load_products()
    categories = []

    for product in products:
        if product.get("active"):
            if product["category"] not in categories:
                categories.append(product["category"])

    return categories


def get_products_by_category(category):
    products = load_products()

    return [
        product
        for product in products
        if product["category"] == category and product.get("active")
    ]


def get_product(product_id):
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            return product

    return None


def buy_product(user_id: int, product_id: str):
    users = load_users()
    products = load_products()

    user_id = str(user_id)

    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "purchases": [],
            "language": "ru"
        }

    product = None

    for item in products:
        if item["id"] == product_id:
            product = item
            break

    if not product:
        return False, "Товар не найден."

    if not product.get("active"):
        return False, "Товар недоступен."

    if users[user_id]["balance"] < product["price"]:
        return False, "Недостаточно средств."

    delivery_type = product.get("delivery_type", "static")

    if delivery_type == "dynamic":
        if not product["content"]:
            return False, "Товар закончился."

        issued_content = product["content"].pop(0)
    else:
        issued_content = product["content"]

    users[user_id]["balance"] -= product["price"]
    users[user_id]["purchases"].append({
        "product_id": product_id,
        "name": product["name"],
        "price": product["price"],
        "content": issued_content
    })

    save_users(users)
    save_products(products)

    product_copy = product.copy()
    product_copy["issued_content"] = issued_content

    return True, product_copy


def add_promocode(code: str, amount: int):
    promocodes = load_promocodes()

    promocodes[code.upper()] = {
        "amount": amount
    }

    save_promocodes(promocodes)


def activate_promocode(user_id: int, code: str):
    promocodes = load_promocodes()
    code = code.upper()

    if code not in promocodes:
        return False, "❌ Промокод не найден или уже использован."

    amount = promocodes[code]["amount"]

    del promocodes[code]
    save_promocodes(promocodes)

    balance = add_balance(user_id, amount)

    return True, (
        f"✅ Промокод активирован!\n\n"
        f"💰 Начислено: {amount} ₽\n"
        f"💵 Баланс: {balance} ₽"
    )