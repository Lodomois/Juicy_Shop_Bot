import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0")
MANAGER_USERNAME = os.getenv("MANAGER_USERNAME", "")

if not BOT_TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN. Добавьте BOT_TOKEN в переменные окружения хостинга.")

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError as exc:
    raise RuntimeError("ADMIN_ID должен быть числом. Проверьте переменные окружения хостинга.") from exc
