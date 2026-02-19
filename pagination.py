import requests

def get_deezer_tracks(playlist_id):
    tracks = []
    
    url = f"https://api.deezer.com/playlist/{playlist_id}"
    response = requests.get(url).json()
    
    # Première page
    data = response["tracks"]
    
    while True:
        # Ajouter les morceaux de la page actuelle
        for track in data["data"]:
            titre = track["title"]
            artiste = track["artist"]["name"]
            tracks.append(f"{titre} {artiste}")
        
        # Vérifier s'il y a une page suivante
        if "next" in data:
            data = requests.get(data["next"]).json()
        else:
            break
    
    return tracks
