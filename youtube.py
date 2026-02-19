from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_youtube_service():
    scopes = ["https://www.googleapis.com/auth/youtube"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        scopes
    )

    credentials = flow.run_console()
    return build("youtube", "v3", credentials=credentials)


def create_playlist(youtube, title):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]


def add_videos(youtube, playlist_id, tracks):
    for track in tracks:
        search = youtube.search().list(
            q=track,
            part="snippet",
            type="video",
            maxResults=1
        ).execute()

        if search["items"]:
            video_id = search["items"][0]["id"]["videoId"]

            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            ).execute()

            print(f"Ajouté : {track}")
