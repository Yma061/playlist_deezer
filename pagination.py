import requests

def get_deezer_tracks(playlist_id):
    tracks = []
    
    # 1️⃣ Récupérer infos playlist
    playlist_url = f"https://api.deezer.com/playlist/{playlist_id}"
    playlist_response = requests.get(playlist_url).json()
    
    # 2️⃣ Récupérer URL tracklist officielle
    tracklist_url = playlist_response["tracklist"]
    
    while tracklist_url:
        response = requests.get(tracklist_url)
        
        if response.status_code != 200:
            print("Erreur API :", response.status_code)
            break
        
        data = response.json()
        
        for track in data["data"]:
            titre = track["title"]
            artiste = track["artist"]["name"]
            tracks.append(f"{titre} {artiste}")
        
        # Pagination
        tracklist_url = data.get("next")
    
    return tracks


if __name__ == "__main__":
    playlist_id = "14838804003"
    
    tracks = get_deezer_tracks(playlist_id)
    
    print(f"{len(tracks)} morceaux récupérés")

