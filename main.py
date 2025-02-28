import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
import google.generativeai as genai
from dotenv import load_dotenv  
import musicLibrary

load_dotenv("key.env")

recognizer = sr.Recognizer()
engine = pyttsx3.init()

newsapi = os.getenv("NEWS_KEY")
gemini_api = os.getenv("GEMINI_KEY")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def aiProcess(command):
    if not gemini_api:
        raise ValueError("GEMINI API key is missing. Check your key.env file.")

    genai.configure(api_key=gemini_api)
    model = genai.GenerativeModel("gemini-1.5-flash")  
    response = model.generate_content(command)
    return response.text

def listen_for_keyword():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Speech recognition service error")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

def get_news_titles():
    if not newsapi:
        raise ValueError("NEWS API key is missing. Check your key.env file.")
    
    url = f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={newsapi}"
    response = requests.get(url)
    if response.status_code == 200:
        news_data = response.json()
        titles = [article['title'] for article in news_data.get('articles', [])]
        return titles
    else:
        print(f"Error {response.status_code}: {response.text}") 
        return ["Failed to fetch news"]

def process_command(command):
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com/")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "news" in command:
        titles = get_news_titles()
        for title in titles:
            print(title)
            speak(title)
    elif command.lower().startswith('play'):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music.get(song, "Song not found")
        webbrowser.open(link)
    else:
        output = aiProcess(command)
        print(output)
        speak(output)

if __name__ == "__main__":
    speak("Initializing Alfred...")
    while True:
        keyword = listen_for_keyword()
        if "alfred" in keyword:
            print("!!Alfred Active!!")
            speak("Yes, how can I assist you?")
            try:
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio).lower()
                    process_command(command)
            except Exception as e:
                print(f"Error: {e}")
