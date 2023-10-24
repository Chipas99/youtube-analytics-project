from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str, api_key) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = api_key

    def print_info(self) -> None:
        try:
            youtube = build('youtube', 'v3', developerKey=self.api_key)
            response = youtube.channels().list(part='snippet,contentDetails,statistics', id=self.channel_id).execute()

            channel_info = response['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            print('Channel Name:', snippet['title'])
            print('Description:', snippet['description'])
            print('Published At:', snippet['publishedAt'])
            print('View Count:', statistics['viewCount'])
            print('Subscriber Count:', statistics['subscriberCount'])
            print('Video Count:', statistics['videoCount'])

        except HttpError as e:
            print(f'An HTTP error {e.resp.status} occurred: {e.content}')
