from vkbottle import API

from data.config import USER_TOKEN


async def search_users(offset, status, sex, age_from, age_to, city):
    api = API(USER_TOKEN)
    users = await api.users.search(
        fields=['domain', 'status', 'sex', 'bdate', 'city', 'country', 'photo_400'],
        count=10, status=status, age_from=age_from, age_to=age_to, sex=sex, hometown=city, has_photo=True,
        is_closed=False, offset=offset, can_access_closed=True, sort=1)
    return users


async def get_photos(user_id):
    try:
        api = API(USER_TOKEN)
        response_photo = await api.photos.get_all(user_id, count=3)
        items = response_photo.items
        photos = [item.sizes[4].url for item in items if len(item.sizes) >= 4]
    except:
        photos = []
    return photos


async def get_data_user(user_id):
    api = API(USER_TOKEN)
    users_info = await api.users.get(user_id,
                                     fields=['domain', 'sex', 'bdate', 'status', 'country', 'city', 'photo_400'])
    response_user = users_info[0]
    photos = await get_photos(user_id)

    return response_user, photos
