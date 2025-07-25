import requests
import speech_recognition as sr
import keyboard
import openai
import pyttsx3
import subprocess
import pyautogui
import webbrowser
import datetime
import time
import ctypes
import json
import os
from dotenv import load_dotenv
from ecapture import ecapture as ec
from urllib.request import urlopen

# Load environment variables
load_dotenv()

# Load API keys securely from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Set OpenAI API key globally
openai.api_key = OPENAI_API_KEY

conversation = []

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def say(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        say("Hello, Good Morning. I am PROTO")
    elif hour < 18:
        say("Hello, Good Afternoon. I am PROTO")
    else:
        say("Hello, Good Evening. I am PROTO")

def date():
    now = datetime.datetime.now()
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                   'September', 'October', 'November', 'December']
    ordinalnames = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                    '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th',
                    '21st', '22nd', '23rd', '24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    say("Today is " + month_names[now.month - 1] + " " + ordinalnames[now.day - 1])
    return f"Today is {month_names[now.month - 1]} {ordinalnames[now.day - 1]}"

def takeCommand():
    say("Press Alt + Ctrl to speak, Sir")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            keyboard.wait("ctrl+alt")
            print("Listening...")
            audio_data = r.listen(source, phrase_time_limit=5)
            print("Recognizing...")
            try:
                text = r.recognize_google(audio_data)
                print(f"User said: {text}")
                return text
            except Exception:
                return "Some Error Occurred. Sorry from Proto"

def weather():
    base_url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}"
    say("City name")
    print("City name: ")
    city = takeCommand()
    complete_url = base_url + "&q=" + city + "&aqi=yes"
    res = requests.get(complete_url).json()
    temp1 = res["current"]["condition"]["text"]
    temp2 = res["current"]["temp_c"]
    name = res["location"]["name"]
    say(f"Today in {name}, the temperature is {temp2}°C. Weather is {temp1}.")
    return f"Today in {name}, the temperature is {temp2}°C. Weather is {temp1}."

def Action(send):
    while True:
        text = send.lower()
        try:
            sites = [["youtube", "https://www.youtube.com"],
                     ["wikipedia", "https://www.wikipedia.com"],
                     ["Chat GPT", "https://platform.openai.com/playground/chat"]]

            for site in sites:
                if f"open {site[0]}" in text:
                    say(f"Opening {site[0]} sir...")
                    webbrowser.open(site[1])
                    return f"{site[0]} Opened Sir"

            if "notepad" in text:
                say("Opening notepad")
                subprocess.Popen(['C:\Windows\System32\\notepad.exe'])
                return "The notepad is open, Sir"

            elif "search google for" in text:
                query = text.split("search google for ")[1]
                say(f"Searching Google for {query}")
                query = query.replace(" ", "+")
                os.system(f"start https://www.google.com/search?q={query}")
                return f"The search for {query} is opened"

            elif "weather" in text:
                return weather()

            elif "show date and time" in text:
                a = date()
                say("Current time is " + datetime.datetime.now().strftime("%I:%M"))
                return a + ". Current time is " + datetime.datetime.now().strftime("%I:%M")

            elif "camera" in text or "take a photo" in text:
                ec.capture(0, "Proto Camera", "img.jpg")
                say("Captured Sir")
                return "Captured Sir"

            elif "lock window" in text:
                pyttsx3.speak("locking the device")
                ctypes.windll.user32.LockWorkStation()
                return "Locked Window Sir"

            elif "screenshot" in text:
                say("Name of the screenshot file")
                name = takeCommand()
                time.sleep(4)
                img = pyautogui.screenshot()
                img.save(f'{name}.png')
                say("Screenshot saved")
                return "Screenshot saved"

            elif "news" in text:
                try:
                    jsonObj = urlopen(f"https://newsapi.org/v2/everything?domains=wsj.com&apiKey={NEWS_API_KEY}")
                    data = json.load(jsonObj)
                    item = data['articles'][0]
                    title = item['title']
                    say('Here is the top news from the Wall Street Journal')
                    say(title)
                    return title
                except Exception as e:
                    return str(e)

            elif "computer" in text:
                query = text.split("computer ")[1]
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=query,
                    temperature=1,
                    max_tokens=256
                )
                reply = response.choices[0].text.strip()
                say(reply)
                return reply

            elif " gpt" in text:
                query = text.split("gpt ")[1]
                conversation.append({"role": "user", "content": query})
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    temperature=0.7,
                    max_tokens=50,
                    messages=conversation
                )
                reply = response['choices'][0]['message']['content']
                say(reply)
                return reply

            else:
                say('Command not recognized, TRY AGAIN')
                return 'Command not recognized, TRY AGAIN'

        except sr.UnknownValueError:
            return "Unable to recognize speech"
        except sr.RequestError as e:
            return f"Error occurred: {e}"

if __name__ == '__main__':
    print('Welcome to PROTO')
    wishMe()
    print("How can I assist you today?")
    say("How can I assist you today?")
    exec(open(r"C:\Users\Tanusri Nukala\PycharmProjects\PROTO2\gui.py").read())
