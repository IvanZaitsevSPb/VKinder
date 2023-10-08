from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import TelegramObject, Chat


class IsPrivate(BaseFilter):
    """
    Фильтр проверяет, является ли чат приватным.
    """

    async def __call__(self, event: TelegramObject, event_chat: Chat) -> bool:
        """
        Вызов фильтра

        :param event: The event object (e.g., Message) to check.
        :param event_chat: The chat object associated with the event.
        :return: True if the message is in a private chat, False otherwise.
        """
        return event_chat.type == ChatType.PRIVATE

class IsGroup(BaseFilter):
    """
    Фильтр проверяет, является ли чат группой.
    """

    async def __call__(self, event: TelegramObject, event_chat: Chat) -> bool:
        """
        Вызов фильтра

        :param event: The event object (e.g., Message) to check.
        :param event_chat: The chat object associated with the event.
        :return: True if the message is in a Group chat, False otherwise.
        """
        return event_chat.type == ChatType.GROUP