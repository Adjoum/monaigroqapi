import os
import streamlit as st
from groq import Groq
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic
from dotenv import load_dotenv
# Importer les fonctions de actions.py
from actions import analyze_and_respond

# Load environment variables
load_dotenv()

# Initialisation de l'API Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])


# Style personnalisé
class CustomStyle(Style):
    background_color = "#272822"  # Fond sombre
    styles = {
        Keyword: "#FF79C6",  # Rose
        Name: "#50FA7B",  # Vert
        Comment: "#6272A4",  # Gris bleu
        String: "#F1FA8C",  # Jaune
        Error: "#FF5555",  # Rouge
        Number: "#BD93F9",  # Violet
        Operator: "#FFB86C",  # Orange
        Generic: "#FFFFFF",  # Blanc
    }

# Fonction pour la coloration syntaxique
def highlight_text(text, style):
    highlighted_code = highlight(text, PythonLexer(), HtmlFormatter(style=style))
    return highlighted_code

# Initialisation de la session Streamlit pour l'historique de la conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ajout de styles CSS personnalisés
st.markdown(
    """
    <style>
    .css-1aumxhk { /* Classe de Streamlit pour le titre de l'application */
        position: sticky;
        top: 0;
        z-index: 1000;
    }

    .css-hi6a2p { /* Classe de Streamlit pour la barre d'entrée */
        position: fixed;
        bottom: 0;
        z-index: 1000;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar gauche avec les options de modèle et de style
with st.sidebar:
    st.title("Options")
    model_name = st.selectbox("Choisissez un modèle LLM", ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma-7b-it"])
    style_name = st.selectbox("Choisissez un style", ["CustomStyle", "monokai", "vim", "vs", "tango", "fruity"])

# Interface principale de l'application
st.title("Modèle IA de ADJOUMANI")

# Affichage de l'historique de la conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie pour l'utilisateur
if user_query := st.chat_input("Entrez votre prompt ici:"):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Condition pour exécuter Groq seulement si actions.py ne comprend pas
    if analyze_and_respond(user_query) == "Je n'ai pas compris votre demande. Veuillez reformuler votre requête.":
        with st.chat_message("assistant"):
            # Construction du prompt avec l'historique de la conversation
            user_query = "Historique:\n" + "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": user_query}],  # Utiliser le prompt avec l'historique
                model=model_name
            )
            response_text = chat_completion.choices[0].message.content

            # Affichage de la réponse de Groq (correctement indenté)
            if style_name == "CustomStyle":
                st.write(highlight_text(response_text, style=CustomStyle), unsafe_allow_html=True)
            else:
                st.write(highlight_text(response_text, style=get_style_by_name(style_name)), unsafe_allow_html=True)
            
            # Mise à jour de l'historique de la conversation
            st.session_state.messages.append({"role": "assistant", "content": response_text})
    
    else:
        response_text = analyze_and_respond(user_query)

        # Affichage de la réponse de actions.py
        if style_name == "CustomStyle":
            st.write(highlight_text(response_text, style=CustomStyle), unsafe_allow_html=True)
        else:
            st.write(highlight_text(response_text, style=get_style_by_name(style_name)), unsafe_allow_html=True)

        # Mise à jour de l'historique de la conversation
        st.session_state.messages.append({"role": "assistant", "content": response_text})