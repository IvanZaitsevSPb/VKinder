from vkbottle import Keyboard, KeyboardButtonColor, Text

keyboard_start = Keyboard(one_time=True, inline=False)
keyboard_start.add(Text("Зарегистрироваться"), color=KeyboardButtonColor.POSITIVE)

keyboard_reg_1 = Keyboard(one_time=True, inline=False)
keyboard_reg_1.add(Text("Мужской"), color=KeyboardButtonColor.POSITIVE)
keyboard_reg_1.row()
keyboard_reg_1.add(Text("Женский", payload={"command": 2}))

keyboard_reg_2 = Keyboard(one_time=True, inline=False)
keyboard_reg_2.add(Text("18 - 22"))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("22 - 26", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("26 - 30", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("30 - 35", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("35 - 40", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("40 - 50", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("50 - 60", payload={"command": 2}))
keyboard_reg_2.row()
keyboard_reg_2.add(Text("60 - 80", payload={"command": 2}))


def keyboard_reg_func(value):
    keyboard_reg_4 = Keyboard(one_time=True, inline=False)
    keyboard_reg_4.add(Text(value), color=KeyboardButtonColor.POSITIVE)
    keyboard_reg_4.row()
    keyboard_reg_4.add(Text("В активном поиске", payload={"command": 2}))
    keyboard_reg_4.row()
    keyboard_reg_4.add(Text("Всё сложно", payload={"command": 2}))
    return keyboard_reg_4


keyboard_about_handler = Keyboard(one_time=True, inline=False)
keyboard_about_handler.add(Text("Да"), color=KeyboardButtonColor.POSITIVE)
keyboard_about_handler.row()
keyboard_about_handler.add(Text("Нет", payload={"command": 2}))

keyboard_check_search = Keyboard(one_time=True, inline=False)
keyboard_check_search.add(Text("Искать"))
keyboard_check_search.row()
keyboard_check_search.add(Text("Меню", payload={"command": 2}))

keyboard_find_half = Keyboard(one_time=True, inline=False)
keyboard_find_half.add(Text("Следующая анкета ->"), color=KeyboardButtonColor.POSITIVE)
keyboard_find_half.row()
keyboard_find_half.add(Text("Меню", payload={"command": 2}))

keyboard_menu = Keyboard(one_time=True, inline=False)
keyboard_menu.add(Text("Искать"))
keyboard_menu.row()
keyboard_menu.add(Text("Сбросить прогресс", payload={"command": 2}))
