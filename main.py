import json
import os
from os.path import dirname, join
import datetime
import time
from typing import Optional

import spotipy
import requests
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
import mysql.connector

import DbModule

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class Music_saver:
   def __init__(self):
      self.db = DbModule.DbModule()
      self.colums = ["track_id", "track", "time", "album", "play_time"]
      self.sp = spotipy.Spotify(
          auth_manager=SpotifyOAuth(
              client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
              client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
              redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
              scope="user-read-currently-playing playlist-modify-public"),
          language='ja')
      self.interval = 60

   def get_song_data(self) -> Optional[list]:
      try:
         current_playing = self.sp.current_user_playing_track()
         if current_playing is None:
            self.interval = 60
            return None
         track_id = current_playing['item']['id']
         track_name: str = current_playing['item']['name']  # 曲名
         artist_name: list = [name["name"] for name in current_playing["item"]["artists"]]  # アーティスト
         duration: int = current_playing["item"]["duration_ms"]  # 再生時間
         self.interval = (duration - current_playing["progress_ms"]) // 1000  # インターバル
         playing_time: str = str(datetime.datetime.now()).split(".")[0]
         album: str = current_playing["item"]["album"]["name"]  # アルバム
         minutes: int = duration // 60000
         seconds: int = (duration - (minutes * 60000)) // 1000
         seconds = str(seconds).zfill(2)
         return [track_id, track_name, f"{minutes}:{seconds}", album, playing_time, artist_name]
      except requests.exceptions.ConnectionError:
         return None
      except requests.exceptions.ReadTimeout:
         return None
      except TypeError:
         return None
      except spotipy.exceptions.SpotifyException:
         return None

   def main(self):
      track_id: str = ""
      while True:
         datas = self.get_song_data()
         if datas is not None and track_id != datas[0]:
            try:
               self.db.multiple_insert("music", self.colums, datas[0:5])
               for artist in datas[5]:
                  self.db.insert("artists", {"track_id": datas[0], "artist": artist})
               track_id = datas[0]
            except mysql.connector.errors.ProgrammingError:
               pass
         time.sleep(self.interval)


if __name__ == '__main__':
   music = Music_saver()
   music.main()
