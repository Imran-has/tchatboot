import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from PIL import Image
import numpy as np
import tempfile
import pygame

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def text_to_speech_urdu(text):
    """Convert text to Urdu speech"""
    try:
        # Generate the speech file
        tts = gTTS(text=text, lang='ur')
        temp_file_path = os.path.join(os.getcwd(), "temp_audio.mp3")  # Save in the current working directory
        tts.save(temp_file_path)

        # Initialize pygame mixer and play the audio
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file_path)
        pygame.mixer.music.play()

        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            continue

        # Clean up the temporary file
        os.remove(temp_file_path)
    except Exception as e:
        st.error(f"Error in text-to-speech: {e}")

def speech_to_text():
    """Convert speech to text"""
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language='ur-PK')
            return text
        except sr.UnknownValueError:
            st.error("Could not understand the audio")
            return None
        except sr.RequestError:
            st.error("Could not request results")
            return None
        except Exception as e:
            st.error(f"Error in speech-to-text: {e}")
            return None

def capture_photo():
    """Capture a photo using the webcam or upload a photo"""
    st.write("آپ اپنی تصویر اپ لوڈ کریں یا کیمرے سے تصویر لیں")
    # Webcam input
    captured_image = st.camera_input("Capture your photo using the webcam")
    if captured_image is not None:
        # Read the captured image as a PIL image
        image = Image.open(captured_image)
        return np.array(image)

    # File uploader as a fallback
    uploaded_file = st.file_uploader("Alternatively, upload your photo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Read the uploaded file as an image
        image = Image.open(uploaded_file)
        return np.array(image)

    return None

def main():
    st.title("اردو رجسٹریشن فارم")
    st.write("Welcome to Urdu Registration Form")

    if 'step' not in st.session_state:
        st.session_state.step = 0
        st.session_state.responses = {}

    if st.session_state.step == 0:
        if st.button("شروع کریں (Start)"):
            text_to_speech_urdu("آپ کا نام کیا ہے؟")
            st.session_state.step = 1

    elif st.session_state.step == 1:
        st.write("آپ کا نام کیا ہے؟")
        if st.button("بولیں (Speak)"):
            name = speech_to_text()
            if name:
                st.session_state.responses['name'] = name
                st.write(f"آپ کا نام: {name}")
                st.session_state.step = 2
                text_to_speech_urdu("آپ کی عمر کیا ہے؟")

    elif st.session_state.step == 2:
        st.write("آپ کی عمر کیا ہے؟")
        age = st.number_input("Age", min_value=0, max_value=150)
        if st.button("Next"):
            if age > 60:
                st.error("معذرت، آپ کی عمر زیادہ ہے")
                text_to_speech_urdu("معذرت، آپ کی عمر زیادہ ہے")
                st.session_state.step = 0
            else:
                st.session_state.responses['age'] = age
                st.session_state.step = 3
                text_to_speech_urdu("آپ کی جنس کیا ہے؟")

    elif st.session_state.step == 3:
        st.write("آپ کی جنس کیا ہے؟")
        if st.button("بولیں (Speak)"):
            gender = speech_to_text()
            if gender:
                st.session_state.responses['gender'] = gender
                st.write(f"آپ کی جنس: {gender}")
                st.session_state.step = 4
                text_to_speech_urdu("آپ کے سربراہ کا شناختی کارڈ نمبر کیا ہے؟")

    elif st.session_state.step == 4:
        st.write("آپ کے سربراہ کا شناختی کارڈ نمبر کیا ہے؟")
        nic = st.text_input("NIC Number", key="nic")
        if st.button("Next"):
            if len(nic) == 13 and nic.isdigit():
                st.session_state.responses['nic'] = nic
                st.session_state.step = 5
                text_to_speech_urdu("براہ کرم اپنی تصویر اپ لوڈ کریں یا کیمرے سے تصویر لیں")
            else:
                st.error("براہ کرم درست شناختی کارڈ نمبر درج کریں")

    elif st.session_state.step == 5:
        st.write("اپنی تصویر اپ لوڈ کریں یا کیمرے سے تصویر لیں")
        photo = capture_photo()
        if photo is not None:
            st.image(photo, caption="آپ کی تصویر")
            st.session_state.responses['photo'] = photo
            st.session_state.step = 6
        else:
            st.error("براہ کرم تصویر اپ لوڈ کریں یا کیمرے سے تصویر لیں")

    elif st.session_state.step == 6:
        st.success("رجسٹریشن مکمل ہو گئی!")
        text_to_speech_urdu("آپ کی رجسٹریشن مکمل ہو گئی ہے۔ شکریہ")
        st.write("### Submitted Information:")
        for key, value in st.session_state.responses.items():
            if key != 'photo':
                st.write(f"{key}: {value}")
        if 'photo' in st.session_state.responses:
            st.image(st.session_state.responses['photo'], caption="Captured Photo")

        if st.button("نئی رجسٹریشن (New Registration)"):
            st.session_state.step = 0
            st.session_state.responses = {}
            st.experimental_rerun()

if __name__ == "__main__":
    main()