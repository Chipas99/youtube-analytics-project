import datetime
from config import YT_API_KEY
from googleapiclient.discovery import build
from operator import itemgetter
import isodate

class PlayList:
    BASE_URL = "https://www.youtube.com/playlist?list="
    BASE_VIDEO_URL = "https://youtu.be/"

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
        self._title = None  # Мы кэшируем заголовок и видео после их загрузки.
        self._videos = None

    @property
    def title(self):
        if self._title is None:
            response = self.youtube.playlists().list(part="snippet", id=self.playlist_id).execute()
            self._title = response['items'][0]['snippet']['title']
        return self._title

    @property
    def url(self):
        return self.BASE_URL + self.playlist_id

    @property
    def videos(self):
        if self._videos is None:
            response = self.youtube.playlistItems().list(
                part="contentDetails", maxResults=50, playlistId=self.playlist_id
            ).execute()
            self._videos = []
            for item in response['items']:
                video_id = item['contentDetails']['videoId']
                video_info = self.youtube.videos().list(part='snippet,statistics,contentDetails', id=video_id).execute()['items'][0]
                duration = isodate.parse_duration(video_info['contentDetails']['duration']) # use isodate.parse_duration
                likes = int(video_info['statistics'].get('likeCount', 0))
                self._videos.append({
                    'id': video_id,
                    'duration': duration,
                    'likes': likes,
                })
        return self._videos

    @property
    def total_duration(self):
        return sum((video['duration'] for video in self.videos), datetime.timedelta()) # handled as timedelta

    def show_best_video(self):
        best_video = max(self.videos, key=itemgetter('likes'))
        return self.BASE_VIDEO_URL + best_video['id']
