import yt_dlp
import os
import re

def sanitize_filename(filename):
    """
    Nettoie une chaîne de caractères pour qu'elle puisse être utilisée comme nom de fichier.
    Supprime les caractères invalides et les remplace par un underscore.
    """
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_and_convert_playlist(playlist_url, output_folder='playlists'):
    """
    Télécharge une playlist YouTube, convertit chaque vidéo en MP3 et l'organise
    dans un dossier portant le nom de la playlist.

    Args:
        playlist_url (str): L'URL de la playlist YouTube.
        output_folder (str): Le dossier parent où les playlists seront sauvegardées.
    """
    print(f"Traitement de la playlist : {playlist_url}")

    # --- Configuration pour yt-dlp ---
    # C'est ici que toute la magie opère.
    ydl_opts = {
        # Options de format : on veut le meilleur audio possible
        'format': 'bestaudio/best',

        # Options de post-traitement (conversion)
        'postprocessors': [{
            # Clé pour la conversion en audio
            'key': 'FFmpegExtractAudio',
            # Format de sortie souhaité
            'preferredcodec': 'mp3',
            # Qualité audio (bitrate). 192 est un bon compromis.
            'preferredquality': '192',
        }],

        # Options de nommage des fichiers et de sortie
        'outtmpl': {
            # Définit le chemin de sortie pour chaque fichier.
            # %(playlist_title)s : Titre de la playlist
            # %(title)s - %(uploader)s : Titre de la vidéo suivi du nom de la chaîne
            # %(ext)s : Extension du fichier (sera .mp3 grâce au post-processeur)
            'default': os.path.join(output_folder, '%(playlist_title)s', '%(title)s - %(uploader)s.%(ext)s'),
        },
        
        # Pour éviter de télécharger à nouveau les fichiers qui existent déjà
        'nooverwrites': True,
        # Pour continuer les téléchargements interrompus
        'continue_dl': True,
    }

    try:
        # On crée une instance de YoutubeDL avec nos options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # On lance le processus de téléchargement pour la playlist
            print("Lancement du téléchargement et de la conversion...")
            ydl.download([playlist_url])
            print("\nOpération terminée avec succès !")
            print(f"Les fichiers ont été sauvegardés dans un sous-dossier de '{output_folder}'.")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nERREUR : Une erreur de téléchargement est survenue : {e}")
        print("Vérifie que l'URL de la playlist est correcte et que la playlist est publique.")
    except Exception as e:
        print(f"\nERREUR : Une erreur inattendue est survenue : {e}")

# --- Point d'entrée du programme ---
if __name__ == "__main__":
    # Remplace cette URL par l'URL de la playlist YouTube que tu veux télécharger.
    # Exemple : "https://www.youtube.com/playlist?list=PL4o29bINVT4EG_y-k5jGoOu3-Am8Nvi10"
    playlist_url_input = input("Veuillez entrer l'URL de la playlist YouTube : ")

    if playlist_url_input:
        # On appelle la fonction principale avec l'URL fournie par l'utilisateur
        download_and_convert_playlist(playlist_url_input)
    else:
        print("Aucune URL fournie. Le programme va se fermer.")