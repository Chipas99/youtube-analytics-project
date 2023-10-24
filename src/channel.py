import requests

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = 'UCthfjHehYgSyhf8ONjzJMUw'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        api_key = "AIzaSyCBkEoN98s8GvGgp0qTByAmiWnCZOo7uFo"


        """Формируем URL для получения информации о канале"""
        url = f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={self.channel_id}&key={api_key}"


        """Отправляем GET-запрос к API"""

        response = requests.get(url)
        data = response.json()

        """Парсим полученные данные и выводим информацию о канале"""

        channel_title = data["items"][0]["snippet"]["title"]
        channel_description = data["items"][0]["snippet"]["description"]
       # channel_subscriber_count = data["items"][0]["statistics"]["subscriberCount"]

        print("Название канала:", channel_title)
        print("Описание канала:", channel_description)
       # print("Число подписчиков:", channel_subscriber_count)
