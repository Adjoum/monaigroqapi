import datetime
import webbrowser
import os
import time
import wikipedia
from datetime import date
import randfacts
import pyjokes

def get_user_input():
    """Attend la saisie de l'utilisateur et la retourne."""
    user_input = input("Vous: ")
    return user_input

def analyze_and_respond(user_input):
    """Analyse l'entrée utilisateur et génère une réponse textuelle."""

    user_input = user_input.lower() # Convertir l'entrée en minuscules pour faciliter l'analyse

    if 'wikipedia' in user_input:
        query = user_input.replace("wikipedia", "").strip()
        results = wikipedia.summary(query, sentences=1)
        response = f"Selon Wikipédia: {results}"
    elif 'ouvrir youtube' in user_input:
        webbrowser.open("youtube.com")
        response = "J'ouvre YouTube pour vous."
    elif 'ouvrir google' in user_input:
        webbrowser.open("google.com")
        response = "J'ouvre Google pour vous."
    elif 'heure' in user_input:
        response = f"Il est {time.strftime('%H:%M:%S')}."
    elif 'date' in user_input:
        response = f"Aujourd'hui, nous sommes le {date.today()}."
    elif 'musique' in user_input and 'chanson' in user_input:
        music_dir = 'D:\Music' # Remplacez par le chemin de votre dossier de musique
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            response = "Lancement de la première chanson dans votre dossier de musique."
        else:
            response = "Votre dossier de musique semble vide."
    elif 'qui es-tu' in user_input:
        response = "Je suis Adjoumani Koffi, un agent IA conçu pour vous aider."
    elif 'ton nom' in user_input:
        response = "Mon nom est Adjoumani Koffi."
    elif 'fait' in user_input:
        fact = randfacts.get_fact()
        response = f"Le saviez-vous ? {fact}"
    elif 'blague' in user_input:
        joke = pyjokes.get_joke()
        response = f"{joke}"
    elif 'créateur' in user_input:
        response = "Mon créateur est Monsieur Koffi Wilfried Adjoumani, un passionné d'apprentissage et de nouvelles technologies."
    elif 'merci' in user_input:
        response = "De rien !"
    elif 'au revoir' in user_input:
        response = "Au revoir, ravi d'avoir échangé avec vous !"
    else:
        response = "Je n'ai pas compris votre demande. Veuillez reformuler votre requête."

    return response


if __name__ == '__main__':
    print("Bonjour, je suis Madame Emmanuella, la directrice du chr de San-Pedro. Comment puis-je vous aider ?")

    while True:
        user_input = get_user_input()
        response = analyze_and_respond(user_input)
        print(f"Agent IA: {response}")

        if user_input.lower() == 'au revoir':
            break





