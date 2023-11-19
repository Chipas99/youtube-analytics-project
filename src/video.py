from googleapiclient.discovery import build
import os

from src.youtube_exceptions import BrokenVideoId


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str):
        """
        Экземпляр инициализируется id видео и добавляет данные по API.
        А также проводится корректность введённого id видео.
        """
        try:
            self.video: dict = self.get_info_about_video(video_id)
            if not self.video['items']:
                raise BrokenVideoId
            self.video_id: str = video_id
            self.title: str = self.video['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count: int = int(self.video['items'][0]['statistics']['viewCount'])
            self.like_count: int = int(self.video['items'][0]['statistics']['likeCount'])
        except BrokenVideoId:
            self.video_id: str = video_id
            self.title: None = None
            self.url: None = None
            self.view_count: None = None
            self.like_count: None = None

    def get_info_about_video(self, video_id: str) -> dict:
        """
        Получает информацию о видео
        """
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video_id
                                                    ).execute()
        return video_response

    def __str__(self) -> str:
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

