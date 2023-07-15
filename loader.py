from vkbottle import CtxStorage, Bot

from data.config import BOT_TOKEN
from database.db_postgresql import Database

# ----------------------------Database-------------------------------
db = Database()

# ----------------------------Token----------------------------------
ctx = CtxStorage()
bot = Bot(BOT_TOKEN)
