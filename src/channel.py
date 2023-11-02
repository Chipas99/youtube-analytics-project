from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = api_key

        self.title = None
        self.description = None
        self.url = None
        self.subscriber_count = None
        self.video_count = None
        self.view_count = None

        self.get_channel_info()

    @classmethod
    def get_service(cls, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def get_channel_info(self):
        try:
            youtube = self.get_service(self.api_key)  # Передаем параметр api_key методу get_service
            response = youtube.channels().list(part='snippet,contentDetails,statistics', id=self.channel_id).execute()

            channel_info = response['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            self.title = snippet['title']
            self.description = snippet['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.view_count = statistics['viewCount']

        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred')

    def print_info(self):
        """Печатает информацию о канале"""
        print(f"Channel ID: {self.channel_id}")
        print(f"Channel Name: {self.title}")
        print(f"Description: {self.description}")
        print(f"Channel Link: {self.url}")
        print(f"Subscriber Count: {self.subscriber_count}")
        print(f"Video Count: {self.video_count}")
        print(f"View Count: {self.view_count}")

    def to_json(self, filename):
        data = {
             'channel_id': self.channel_id,
             'channel_name': self.title,
             'description': self.description,
             'channel_link': self.url,
             'subscriber_count': self.subscriber_count,
             'video_count': self.video_count,
             'view_count': self.view_count
        }

        with open(filename, 'w') as file:
            json.dump(data, file)

    def __str__(self):
        """Возвращает название и ссылку на канал"""
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """Складывает два канала по количеству подписчиков"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        """Вычитает количество подписчиков другого канала из текущего"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    '''методы сравнения __gt__, __ge__, __lt__, __le__, __eq__ и __ne__'''
    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __ne__(self, other):
        return self.subscriber_count != other.subscriber_count
