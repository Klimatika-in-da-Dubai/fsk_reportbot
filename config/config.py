from envparse import env
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = env.str("TELEGRAM_TOKEN")
