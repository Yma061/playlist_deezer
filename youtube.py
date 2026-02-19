from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def get_youtube_service():
    scopes = ["https://www.googleapis.com/auth/youtube"]

    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        scopes=scopes
    )

    auth_url, _ = flow.authorization_url(prompt="consent")

    print("Va sur cette URL pour autoriser l'application :")
    print(auth_url)

    code = input("Colle le code ici : ")

    flow.fetch_token(code=code)

    credentials = flow.credentials

    return build("youtube", "v3", credentials=credentials)
