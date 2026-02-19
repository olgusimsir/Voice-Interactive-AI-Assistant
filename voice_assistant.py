"""
Voice Interactive AI Assistant
Author: Olgu Şimşir
Description:
A real-time conversational voice assistant using
Speech Recognition + OpenAI GPT + Text-to-Speech.
"""

import speech_recognition as sr
from gtts import gTTS
from pygame import mixer
import time
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Conversation memory
messages_array = [
    {"role": "system", "content": "You are my AI assistant"}
]

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        messages_array.append({"role": "user", "content": query})
        respond()
    except Exception as e:
        print("Speech recognition error:", e)
        listen()

def respond():
    print("Responding...")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_array
    )

    reply = res.choices[0].message.content
    messages_array.append({"role": "assistant", "content": reply})

    speak(reply)

def speak(text):
    speech = gTTS(text=text, lang="en", slow=False)
    speech.save("captured_voice.mp3")

    mixer.init()
    mixer.music.load("captured_voice.mp3")
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)

    mixer.music.unload()
    mixer.quit()

    os.remove("captured_voice.mp3")

    listen()

def main():
    print("Voice Assistant Started...")
    listen()

if __name__ == "__main__":
    main()
