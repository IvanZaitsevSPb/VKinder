from vkbottle import BaseStateGroup


class Registration(BaseStateGroup):
    gender = "gender"
    age = "age"
    city = "city"
    status = "status"


class YesOrNo(BaseStateGroup):
    check = "check"
