from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
USER_TOKEN = env.str("USER_TOKEN")

DB_USER = env.str("DB_USERNAME")
DB_PASS = env.str("DB_PASSWORD")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")
