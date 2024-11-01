import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotifyの認証情報を設定
client_id = 'e8af0f9f75b34102bd425b84704d5722'
client_secret = '3e61db7bc0eb49a2ba774ddfade07ff9'
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# ユーザーに曲名とアーティスト名を入力してもらう
track_name = input("曲名を入力してください: ")
artist_name = input("アーティスト名を入力してください: ")

# 曲をSpotifyから検索
try:
    results = sp.search(q=f'artist:"{artist_name}" track:"{track_name}"', type='track', limit=1)
    track = results['tracks']['items'][0]
except IndexError:
    print(f"'{artist_name}'の'{track_name}'に一致する曲が見つかりませんでした。")
    exit()

# 曲の詳細情報を取得
track_id = track['id']
audio_features = sp.audio_features(track_id)[0]
album = sp.album(track['album']['id'])

# アーティストのジャンル情報を取得
artist_id = track['artists'][0]['id']
artist = sp.artist(artist_id)
artist_genres = artist['genres']

# アーティストの画像を取得
if len(artist['images']) > 0:
    artist_image_url = artist['images'][0]['url']
else:
    artist_image_url = "画像が見つかりませんでした。"

# 曲のジャンル情報を取得（アルバムのジャンルを使用）
album_genres = album.get('genres', [])

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
    f.write(f"アルバム: {track['album']['name']}\n")
    f.write(f"リリース年: {track['album']['release_date']}\n")
    f.write(f"再生時間: {track['duration_ms'] // 1000}秒\n")
    f.write(f"人気度: {track['popularity']}\n")
    f.write(f"アルバムの種類: {album['album_type']}\n")
    f.write(f"アルバムのトラック数: {album['total_tracks']}\n")
    f.write(f"コピーライト: {album['copyrights'][0]['text']}\n")
    f.write(f"外部URL: {track['external_urls']['spotify']}\n")
    f.write(f"プレビューURL: {preview_url}\n")
    
    # 曲のジャンル情報を追加
    f.write(f"ジャンル: {', '.join(album_genres) if album_genres else 'ジャンル情報なし'}\n")
    
    # 曲の特徴量 (ダンスビート、エネルギーなど)
    f.write("\n-- 曲の特徴量 --\n")
    for feature, value in audio_features.items():
        f.write(f"{feature}: {value}\n")
    f.write(f"テンポ (BPM): {audio_features['tempo']}\n")
    f.write(f"キー: {audio_features['key']}\n")
    f.write(f"モード: {'メジャー' if audio_features['mode'] == 1 else 'マイナー'}\n")
    f.write(f"タイムシグネチャー: {audio_features['time_signature']}\n")
    
    # アーティストの詳細情報を出力
    f.write("\n-- アーティストの詳細情報 --\n")
    f.write(f"アーティスト名: {artist['name']}\n")
    f.write(f"フォロワー数: {artist['followers']['total']}\n")
    f.write(f"人気度: {artist['popularity']}\n")
    f.write(f"ジャンル: {', '.join(artist_genres)}\n")
    f.write(f"外部URL: {artist['external_urls']['spotify']}\n")
    f.write(f"アーティスト画像: {artist_image_url}\n")
    
    # アーティストの人気曲を出力
    f.write("\n-- アーティストの人気曲 --\n")
    for idx, track in enumerate(top_tracks, start=1):
        f.write(f"{idx}. {track['name']} - {track['album']['name']}\n")
    
    # アーティストの関連アーティストを出力
    f.write("\n-- 関連アーティスト --\n")
    for related_artist in related_artists:
        f.write(f"{related_artist['name']} ({related_artist['followers']['total']}フォロワー)\n")

print(f"{track_name}.txtファイルに詳細情報を出力しました。")