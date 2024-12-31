import streamlit as st
import speech_recognition as sr
import os

def transcribe_speech(api_choice, language_choice):
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            st.info("Parlez maintenant...")
            audio_text = r.listen(source)
            st.info("Transcription...")

            # Choix de l'API de reconnaissance vocale
            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=language_choice)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language_choice)
            else:
                text = "API non supportée."

            return text

    except sr.UnknownValueError:
        return "Désolé, je n'ai pas compris la parole."
    except sr.RequestError as e:
        return f"Erreur avec le service de reconnaissance vocale; {e}"
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

def main():
    st.title("Speech Recognition App")

    # Sélection de l'API de reconnaissance vocale
    api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale", ("Google", "Sphinx"))

    # Sélection de la langue
    language_choice = st.selectbox("Choisissez la langue", ("en-US", "fr-FR", "es-ES"))

    st.write("Cliquez sur le microphone pour commencer à parler:")

    # Crée un placeholder pour afficher la transcription
    placeholder = st.empty()

    # Bouton pour commencer l'enregistrement
    if st.button("Start Recording"):
        text = transcribe_speech(api_choice, language_choice)
        
        # Utilisation du placeholder pour afficher la transcription
        placeholder.write(f"Transcription : {text}")

        # Enregistrer le texte transcrit dans un fichier
        if st.button("Enregistrer le texte dans un fichier"):
            with open("transcription.txt", "w") as file:
                file.write(text)
            st.success("Le texte a été enregistré avec succès.")

    # Fonctionnalité de pause et reprise
    if st.button("Pause Recording"):
        st.write("Enregistrement mis en pause...")

    if st.button("Reprendre Recording"):
        st.write("Reprise de l'enregistrement...")

if __name__ == "__main__":
    main()
