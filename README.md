# Spotify MusicSaver
Spotifyで聞いた曲の履歴を保存するやつ

保存した履歴からプレイリストを使うなり、データ解析の素材にするなり

## 特徴

ただ保存するだけではなく、ちゃんと聞いた曲だけを保存するようにしています。
仕組みとしては、再生曲の時間と再生時の曲の時間から差を出して、これが一定値を下回る、つまりおおよそ最後まで聞くとデータベースに保存されます。

なので間違えて変な曲再生してもカウントされません、ご安心を

## 1. pipenvを使う場合
pipenvが必要です。
```sh
$ pip install pipenv
```
インストール後は同様に、以下のコマンドを実行してください。
```sh
$ pipenv install
$ pipenv shell
```

起動するにはmain.pyを実行してください
```sh
$ python main.py
```

<img src="https://github.com/alrab223/Spotify_MusicSaver/blob/master/image/song_analyze.png">

最近集計したやつ