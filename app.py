import asyncio
import logging

from loader import bot, db
import vkbot

logging.getLogger("vkbottle").setLevel(logging.INFO)


async def main():
    # await db.drop_tables()
    await db.create_users_table()
    await db.create_viewed_profiles_table()

    await bot.run_polling()  # Запускаем бота
    await db.close()


if __name__ == '__main__':
    # --------------------------enabling_bot---------------------------
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("Bot stopped!")

