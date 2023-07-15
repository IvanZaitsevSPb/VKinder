from datetime import datetime

from vkbottle.bot import Message

from keyboards import default
from loader import bot, db, ctx
from states.state import Registration, YesOrNo
from vkbot.userbot import get_data_user, search_users, get_photos


async def assemble_profile(response_user, photos, someone=False):
    sex = "Женский" if response_user.sex == 1 else "Мужской"
    photo_urls = '\n\n'.join(photos) if photos else response_user.photo_400
    date_user = response_user.bdate if response_user.bdate and len(
        response_user.bdate.split(".")) == 3 else None
    age_user = (datetime.today() - datetime.strptime(date_user,
                                                     '%d.%M.%Y')).days // 365 if date_user else "возраст скрыт"
    city = response_user.city.title if response_user.city else "Скрыто"
    if someone:
        profile = f"""Имя: {response_user.first_name} {response_user.last_name}
        Город: {city}
        Пол: {sex}
        Возраст: {age_user}
        Ссылка на страницу: @{response_user.domain}
        Фото: {photo_urls}
"""
    else:
        profile = f"""Ваше имя: {response_user.first_name} {response_user.last_name}
        Ваш город: {city}
        Ваш пол: {sex}
        Ваш возраст: {age_user}
        Ссылка на страницу: @{response_user.domain}
        Ваши фото: {photo_urls}"""

    return profile


@bot.on.message(text="Начать")
async def start_handler(message: Message):
    user_id = message.from_id
    users_info = await bot.api.users.get(user_id)

    if await db.get_user(user_id):
        await db.delete_user(user_id)

    await message.answer(
        "Привет, {}. В данном боте ты можешь найти свою вторую половинку".format(users_info[0].first_name),
        keyboard=default.keyboard_start.get_json())


@bot.on.message(text="Зарегистрироваться")
async def registration_1(message: Message):
    await bot.state_dispenser.set(message.peer_id, Registration.gender)
    await message.answer("Какой пол хочешь найти?", keyboard=default.keyboard_reg_1.get_json())


@bot.on.message(state=Registration.gender)
async def registration_2(message: Message):
    ctx.set("gender", message.text)
    await bot.state_dispenser.set(message.peer_id, Registration.age)
    await message.answer("Какой возрастной диапазон интересен?", keyboard=default.keyboard_reg_2.get_json())


@bot.on.message(state=Registration.age)
async def registration_3(message: Message):
    ctx.set("age", message.text)
    await bot.state_dispenser.set(message.peer_id, Registration.city)
    await message.answer("Напиши в каком городе ищешь.")


@bot.on.message(state=Registration.city)
async def registration_4(message: Message):
    ctx.set("city", message.text.strip())
    gender = ctx.get("gender")
    await bot.state_dispenser.set(message.peer_id, Registration.status)
    await message.answer("Какой статус семейного положения?",
                         keyboard=default.keyboard_reg_func(
                             "Не женат" if gender == "Мужской" else "Не замужем").get_json())


@bot.on.message(state=Registration.status)
async def registration_5(message: Message):
    ctx.set("status", message.text)
    user_id = message.from_id
    response_user, photos = await get_data_user(user_id)

    profile = await assemble_profile(response_user, photos)

    ctx.set("purpose_gender", message.text)
    await bot.state_dispenser.set(message.peer_id, YesOrNo.check)

    await message.answer(f"Так ваша анкета отображается в поиске:\n{profile}")
    await message.answer(f"Изменить отображение анкеты можно отредактировав свою страничку ВК.")
    await message.answer(f"Завершить регистрацию?", keyboard=default.keyboard_about_handler.get_json())


@bot.on.message(state=YesOrNo.check)
async def check(message: Message):
    if message.text.lower() == 'да':
        user_id = message.from_id
        user = await db.get_user(user_id)
        if not user:
            await db.add_user(user_id)
        await message.answer("Теперь давай кого-то для тебя найдём", keyboard=default.keyboard_check_search.get_json())
        await bot.state_dispenser.delete(message.peer_id)
        ctx.set("offset", 0)
    else:
        await message.answer("Хорошо, давайте тогда заново", keyboard=default.keyboard_start.get_json())


@bot.on.message(text=["Искать", "Следующая анкета ->"])
async def find_half(message: Message):
    user_id = message.from_id
    gender = ctx.get("gender")
    age_from, age_to = ctx.get("age").split(' - ')
    city = ctx.get("city")
    status = ctx.get("status")

    if status == "Не женат" or status == "Не замужем":
        status_id = '1'
    elif status == "Всё сложно":
        status_id = '5'
    else:
        status_id = '6'

    offset = ctx.get("offset")
    while True:
        users = (await search_users(offset, status=status_id, age_from=age_from, age_to=age_to,
                                    sex=1 if gender == "Женский" else 2, city=city)).items
        if users:
            for user in users:
                offset += 1
                if user.is_closed is False:
                    if not await db.get_viewed_profile(int(str(user_id) + str(user.id))):
                        ctx.set("offset", offset)
                        await db.add_viewed_profile(user_id, user.id)
                        photos = await get_photos(user.id)
                        profile = await assemble_profile(user, photos, someone=True)
                        return await message.answer(profile, keyboard=default.keyboard_find_half)

        return await message.answer("Анкет не осталось!", keyboard=default.keyboard_menu)


@bot.on.message(text="Меню")
async def menu(message: Message):
    await message.answer("Вы можете сбросить свой прогресс поиска и начать заново.",
                         keyboard=default.keyboard_menu.get_json())


@bot.on.message(text="Сбросить прогресс")
async def restart(message: Message):
    await db.delete_user(message.from_id)
    await message.answer("Начните поиск заново!", keyboard=default.keyboard_start.get_json())
