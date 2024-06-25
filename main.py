import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
import requests

# Spotifyの認証情報を設定
client_id = '801c2d22bb02478886affc4ea38f0e45'
client_secret = '88f463df5cb64dd3aebe8ea7cc5f0e0a'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ユーザーに曲名とアーティスト名を入力してもらう
track_name = input("曲名を入力してください: ")
artist_name = input("アーティスト名を入力してください: ")

# 曲を検索
try:
    results = sp.search(q=f'artist:"{artist_name}" track:"{track_name}"', type='track', limit=1)
    track = results['tracks']['items'][0]
except IndexError:
    print(f"'{artist_name}'の'{track_name}'に一致する曲が見つかりませんでした。")
    sys.exit()

# 曲の詳細情報を取得
track_id = track['id']
audio_features = sp.audio_features(track_id)[0]
album = sp.album(track['album']['id'])

# アーティストのジャンル情報を取得
artist_id = track['artists'][0]['id']
artist = sp.artist(artist_id)
artist_genres = artist['genres']

# 歌詞の取得
musixmatch_api_key = 'cd5ec9dc510e035062b134888788d4d3'
musixmatch_base_url = 'https://api.musixmatch.com/ws/1.1/'

try:
    response = requests.get(f'{musixmatch_base_url}track.lyrics.get', 
                            params={'apikey': musixmatch_api_key, 'track_id': track_id})
    lyrics_data = response.json()
    
    # 歌詞データの構造を確認し、適切にアクセスする
    if lyrics_data['message']['header']['status_code'] == 200:
        track_lyrics = lyrics_data['message']['body']['lyrics']['lyrics_body']
    else:
        track_lyrics = "歌詞が見つかりませんでした。"
except (KeyError, requests.RequestException) as e:
    track_lyrics = f"歌詞が見つかりませんでした。エラー: {str(e)}"

# アーティストの画像を取得
if len(artist['images']) > 0:
    artist_image_url = artist['images'][0]['url']
else:
    artist_image_url = "画像が見つかりませんでした。"

# 曲のプレビューURLの取得
preview_url = track['preview_url'] if 'preview_url' in track else "プレビューがありません。"

# アーティストの人気曲の取得
top_tracks = sp.artist_top_tracks(artist_id, country='US')['tracks']

# アーティストの関連アーティストの取得
related_artists = sp.artist_related_artists(artist_id)['artists']

# 曲の詳細情報をテキストファイルに出力
with open(f"{track_name}.txt", "w", encoding="utf-8") as f:
    f.write(f"曲名: {track['name']}\n")
    f.write(f"アーティスト: {', '.join(artist['name'] for artist in track['artists'])}\n")
    
    # 曲のジャンル情報が存在する場合は出力
    if 'genres' in track:
        track_genres = track['genres']
        f.write(f"曲のジャンル: {', '.join(track_genres)}\n")
    else:
        f.write(f"曲のジャンル: なし\n")
    
    # アーティストのジャンル情報を出力
    if artist_genres:
        f.write(f"アーティストのジャンル: {', '.join(artist_genres)}\n")
    else:
        f.write(f"アーティストのジャンル: なし\n")
    
    f.write(f"アルバム: {track['album']['name']}\n")
    f.write(f"リリース年: {track['album']['release_date']}\n")
    f.write(f"再生時間: {track['duration_ms'] // 1000}秒\n")
    f.write(f"人気度: {track['popularity']}\n")
    f.write(f"アルバムの種類: {album['album_type']}\n")
    f.write(f"コピーライト: {album['copyrights'][0]['text']}\n")
    f.write(f"外部URL: {track['external_urls']['spotify']}\n")
    f.write(f"プレビューURL: {preview_url}\n")
    f.write(f"対応市場: {', '.join(sp.track(track_id)['available_markets'])}\n")
    
    # 曲の特徴量 (ダンスビート、エネルギーなど)
    f.write("\n-- 曲の特徴量 --\n")
    for feature, value in audio_features.items():
        f.write(f"{feature}: {value}\n")
    
    # 歌詞を出力
    f.write("\n-- 歌詞 --\n")
    f.write(f"{track_lyrics}\n")
    
    # アーティストの詳細情報を出力
    f.write("\n-- アーティストの詳細情報 --\n")
    f.write(f"アーティスト名: {artist['name']}\n")
    f.write(f"フォロワー数: {artist['followers']['total']}\n")
    f.write(f"人気度: {artist['popularity']}\n")
    f.write(f"ジャンル: {', '.join(artist['genres'])}\n")
    f.write(f"外部URL: {artist['external_urls']['spotify']}\n")
    f.write(f"アーティスト画像: {artist_image_url}\n")
    
    # アーティストの人気曲を出力
    f.write("\n-- アーティストの人気曲 --\n")
    for idx, track in enumerate(top_tracks, start=1):
        f.write(f"{idx}. {track['name']} - {track['album']['name']}\n")
