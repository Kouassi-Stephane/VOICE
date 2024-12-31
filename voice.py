import streamlit as st
import speech_recognition as sr
import os

# Fonction pour transcrire la parole en texte
def transcribe_speech(api_choice, language_choice):
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Parlez maintenant...")
            audio_text = r.listen(source)
            st.info("Transcription en cours...")

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
        return f"Erreur avec le service de reconnaissance vocale : {e}"
    except Exception as e:
        return f"Une erreur s'est produite : {e}"

# Fonction principale
def main():
    st.title("Speech Recognition App")

    # Initialisation de l'état de la transcription
    if "transcription" not in st.session_state:
        st.session_state.transcription = ""

    # Sélection de l'API de reconnaissance vocale
    api_choice = st.selectbox("Choisissez l'API de reconnaissance vocale", ("Google", "Sphinx"))

    # Sélection de la langue
    language_choice = st.selectbox("Choisissez la langue", ("en-US", "fr-FR", "es-ES"))

    st.write("Cliquez sur le microphone pour commencer à parler :")

    # Bouton pour commencer l'enregistrement
    if st.button("Start Recording"):
        st.session_state.transcription = transcribe_speech(api_choice, language_choice)
        st.write("Transcription : ", st.session_state.transcription)

        # Sauvegarder automatiquement dans un fichier
        try:
            file_path = os.path.join(os.getcwd(), "transcription.txt")
            with open(file_path, "w") as file:
                file.write(st.session_state.transcription)
            st.success(f"Le texte a été enregistré avec succès dans : {file_path}")
        except Exception as e:
            st.error(f"Erreur lors de la création du fichier : {e}")

    # Afficher la transcription actuelle
    if st.session_state.transcription:
        st.write("Texte transcrit :")
        st.text_area("Transcription", st.session_state.transcription, height=200)

if __name__ == "__main__":
    main()
