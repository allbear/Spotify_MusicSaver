import os
from os.path import dirname, join
import datetime
import time
from typing import Optional
import traceback

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
      self.sp = spotipy.Spotify(
          auth_manager=SpotifyOAuth(
              client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
              client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
              redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
              scope="user-read-currently-playing playlist-modify-public"),
          language='ja')
      self.interval = 30  # 初期の再生されているかを確認する間隔
      self.track_id_que = ""

   def get_song_data(self) -> Optional[list]:
      try:
         current_playing = self.sp.current_user_playing_track()
         # 曲が再生されていない、中断されている場合、何もしない
         if current_playing is None or current_playing["is_playing"] is False:
            self.interval = 30
            return False, [], [], 0
         track_id = current_playing['item']['id']
         track_name: str = current_playing['item']['name']  # 曲名
         artists: list = [name["name"] for name in current_playing["item"]["artists"]]  # アーティスト
         duration: int = current_playing["item"]["duration_ms"]  # 再生時間
         self.interval = (duration - current_playing["progress_ms"]) // 1000  # インターバル(ms → s)
         playing_time: str = str(datetime.datetime.now()).split(".")[0]
         album: str = current_playing["item"]["album"]["name"]  # アルバム名
         minutes: int = duration // 60000
         seconds: int = (duration - (minutes * 60000)) // 1000
         seconds = str(seconds).zfill(2)
         popularity = current_playing['item']["popularity"]
         return True, [track_id, track_name, f"{minutes}:{seconds}", album, playing_time], artists, popularity
      except(spotipy.exceptions.SpotifyException,
             TypeError,
             requests.exceptions.ConnectionError,
             requests.exceptions.ReadTimeout):
         print(traceback.format_exc())
         return None

   def playing_status_confirmation(self, track_id):
      try:
         current_playing = self.sp.current_user_playing_track()
         if current_playing is None:
            return None
         elif track_id != current_playing['item']['id']:
            return "skip"
         elif current_playing["is_playing"] is False:
            return "pause"
         else:
            return "play"

      except(spotipy.exceptions.SpotifyException,
             TypeError,
             requests.exceptions.ConnectionError,
             requests.exceptions.ReadTimeout):
         print(traceback.format_exc())
         return None

   def insert_features(self, track_id):  # 楽曲の特徴を登録
      columns = self.db.get_columns("music_features")
      try:
         audio_f = self.sp.audio_features(track_id)
         del columns[0:2]
         datas = [audio_f[0][x] for x in columns]
         datas[9] = int(datas[9])  # テンポを整数に変換
      except TypeError:  # ローカルの音楽を再生した場合、終了
         return
      self.db.allinsert("music_features", [None, track_id] + datas)

   def get_interval(self):
      current_playing = self.sp.current_user_playing_track()
      duration: int = current_playing["item"]["duration_ms"]  # 再生時間
      return (duration - current_playing["progress_ms"]) // 1000  # インターバル(ms → s)

   def data_regist(self):
      ret, track_datas, artists, popularity = self.get_song_data()
      if ret is False:  # 曲が再生されていないとき、何もしない
         return
      track_id = track_datas[0]
      if self.track_id_que == track_id:  # 同じ曲がダブって登録されないように
         return
      while self.interval >= 5:
         confirmation: str = self.playing_status_confirmation(track_id)

         if confirmation == "skip":  # 再生中に他の曲に変わってたら登録せずに終了
            self.interval = 5  # すぐ次の曲に移れるように5秒に設定
            return
         elif confirmation == "pause":  # ポーズ中は止める
            self.interval = self.get_interval()
         elif confirmation is None:  # 楽曲データが存在しなければ終了
            self.interval = 30
            return
         else:  # play
            self.interval -= 5

         time.sleep(5)
      try:
         for artist in artists:  # 複数アーティストの場合、ループで格納
            self.db.allinsert("artists", [None, track_id, artist])
         self.db.allinsert("popularity", [None, track_id, popularity])
         self.db.allinsert("music", track_datas)
         self.insert_features(track_id)  # 楽曲の特徴を登録
         self.track_id_que = track_id
         self.interval = 5
         print(f"{track_datas[1]}登録しました")
      except mysql.connector.errors.ProgrammingError:
         print(traceback.format_exc())

   def main(self):
      while True:
         self.data_regist()
         time.sleep(self.interval)


if __name__ == '__main__':
   music = Music_saver()
   music.main()
