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

from ecapture import ecapture as ec
from urllib.request import urlopen

conversation=[]
# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the rate of speech
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

# Set the voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Check if the API key is set in the environment variable
api_key = os.environ.get("OPENAI_API_KEY")

if api_key is None:
    # If the API key is not set in the environment variable, you can pass it directly
    api_key = "sk-proj-RHWcWibL9ykJfFWbu1r8T3BlbkFJO8j81t76AQPDVczGtFLW"
# Function to speak the given text

def say(text):
    engine.say(text)
    engine.runAndWait()
def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        say("Hello,Good Morning")
        say("I am PROTO")

    elif hour >= 12 and hour < 18:  # This uses the 24 hour system so 18 is actually 6 p.m
        say("Hello,Good Afternoon")
        say("I am PROTO")

    else:
        say("Hello,Good Evening")
        say("I am PROTO")
def date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()

    month_name = now.month
    day_name = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                   'November', 'December']
    ordinalnames = ['1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
                    '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24rd', '25th',
                    '26th', '27th', '28th', '29th', '30th', '31st']

    say("Today is " + month_names[month_name - 1] + " " + ordinalnames[day_name - 1] + '.')
    print("Today is " + month_names[month_name - 1] + " " + ordinalnames[day_name - 1] + '.')
    return f"Today is " + month_names[month_name - 1] + " " + ordinalnames[day_name - 1] + '.'
def takeCommand():
    say("Press Alt+ Ctrl to speak Sir")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            #print('Welcome to PROTO')
            #say("PROTO")
            print("Ready for speech...")
            # Wait for the keyboard combination to start listening
            keyboard.wait("ctrl+alt")
            print("Listening...")
            # Start listening for audio
            audio_data = r.listen(source, phrase_time_limit=5)
            # Wait for the keyboard combination to stop listening
            print("Recognizing...")

            try:
                # Use Google speech recognition to convert audio to text
                text = r.recognize_google(audio_data)
                print(f"User said: {text}")
                return text
            except Exception as e:
                return "Some Error Occurred. Sorry from Proto"

def weather():
    base_url = "http://api.weatherapi.com/v1/current.json?key=52e0832fb42b47ed8ed122230242904"
    say(" City name ")
    print("City name : ")
    city = takeCommand()
    complete_url = base_url + "&q=" + city + "&aqi=yes"
    res = requests.get(complete_url).json()
    temp1 = res["current"]["condition"]["text"]
    temp2 = res["current"]["temp_c"]
    name = res["location"]["name"]
    say(
        f"Hello Today in {name} the temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}")
    print(
        f"Hello Today in {name} the temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}")
    return f"Hello Today in {name} the temperature is {format(temp2)} degree Celsius \nWeather is {format(temp1)}"

# Initialize the recognizer
def Action(send):
    while True:
        """print("How can I Assist you today?")
        say("How can I Assist you Today?")"""
        text=send.lower()
# Use the default microphone as the audio source
        try:
                # Perform an action based on the recognized text
                sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                         ["Chat GPT", "https://platform.openai.com/playground/chat"]]
                for site in sites:
                    if f"Open {site[0]}".lower() in text.lower():
                        say(f"Opening {site[0]} sir...")
                        webbrowser.open(site[1])
                        say(f"{site[0]} Opened Sir")
                        return(f"{site[0]} Opened Sir")

                if "notepad" in text.lower():
                    say("Opening notepad")
                    subprocess.Popen(['C:\Windows\System32\\notepad.exe'])
                    say(f"The notepad is Open Sir")
                    return f"The notepad is Open Sir"

                elif "search google for" in text.lower():
                    query = text.lower().split("search google for ")[1]
                    say(f"searching google for {query}")
                    query = query.replace(" ", "+")
                    os.system(f"start https://www.google.com/search?q={query}")
                    return f"The search for {query} is opened "

                elif "start spotify" in text.lower():
                    pyttsx3.speak("Pause Music" )
                    exec(open(r"C:\Users\Tanusri Nukala\PycharmProjects\PROTO2\openAndPlay.py").read())
                    say(f"Opened Spotify")
                    return f"Opened spotify Sir"

                elif ("pause music" in text.lower() or "pause song" in text.lower() or "play music" in text.lower()
                      or "resume music" in text.lower()):
                    exec(open(r"C:\Users\Tanusri Nukala\PycharmProjects\PROTO2\pausePlayMusic.py").read())
                    say(f"Done Sir")
                    return f"Done Sir"

                elif "like this song" in text.lower() or "like song" in text.lower():
                    pyttsx3.speak("Liking Song")
                    exec(open(r"C:\Users\Tanusri Nukala\PycharmProjects\PROTO2\likeSong.py").read())
                    say(f"The Song has been liked Sir")
                    return f"The Song has been liked Sir"

                elif "song" in text.lower():
                    pyttsx3.speak("starting music")
                    cPath = r"C:\Users\Tanusri Nukala\Desktop\AI\Shiah Maisel & Clarx - Left With Nothing [NCS Release].mp3"
                    # Replace with the actual path to your music file
                    os.startfile(cPath)
                    say("Playing Music Sir")
                    return f"Playing Music sir"

                elif "weather" in text:
                    return weather()
                    break

                elif "show date and time" in text.lower():
                    a=date()
                    say("Current time is " +
                               datetime.datetime.now().strftime("%I:%M"))
                    return a+f"Current time is " + datetime.datetime.now().strftime("%I:%M")

                elif "camera" in text or "take a photo" in text:
                    ec.capture(0, "Proto Camera ", "img.jpg")
                    say("Captured Sir")
                    return f"Captured Sir"

                elif "restart" in text:
                    pyttsx3.speak("Restarting Sir")
                    #subprocess.call(["shutdown", "/r"])
                    return f"Restarted"

                elif "hibernate" in text or "sleep" in text:
                    pyttsx3.speak("Hibernating")
                    #subprocess.call("shutdown / h")
                    return f"Hibernating"

                elif 'lock window' in text:
                    pyttsx3.speak("locking the device")
                    ctypes.windll.user32.LockWorkStation()
                    return f"Locked Window Sir"

                elif "log off" in text or "sign out" in text:
                    pyttsx3.speak("Make sure all the application are closed before sign-out")
                    time.sleep(5)
                    subprocess.call(["shutdown", "/l"])
                    return f"Shut Downing Sir"

                elif "screenshot" in text:
                    say("name of the screenshot file")
                    name = takeCommand()
                    time.sleep(4)
                    img = pyautogui.screenshot()
                    img.save(f'{name}.png')
                    say("Screenshot saved")
                    return f"Screenshot saved"

                elif 'news' in text:

                    try:
                        jsonObj = urlopen(
                            '''https://newsapi.org/v2/everything?domains=wsj.com&apiKey=f09f0816098b474292baeddb799daeb1''')
                        data = json.load(jsonObj)
                        i = 1
                        pyttsx3.speak('here are some top news from the WALL STREET JOURNAL')
                        print('''=============== WALL STREET JOURNAL ============''' + '\n')
                        for item in data['articles']:
                            print(str(i) + '. ' + item['title'] + '\n')
                            print(item['description'] + '\n')
                            print(item['url'])
                            pyttsx3.speak(str(i) + '. ' + item['title'] + '\n')
                            #i += 1
                            return str(i) + '. ' + item['title']


                    except Exception as e:
                        print(str(e))


                elif "Power".lower() in text.lower():
                    whatsapp_path = r"C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe"
                    os.startfile(whatsapp_path)
                    return f"Opened Power BI"

                elif "Proto Quit".lower() in text.lower():
                    say('goodbye')
                    exit()


                elif "write a note" in text:
                    pyttsx3.speak("What should i write, sir")
                    note = takeCommand()
                    file = open('proto.txt', 'w')
                    pyttsx3.speak("Sir, Should i include date and time")
                    m = takeCommand()
                    if 'yes' in m or 'sure' in m:
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        file.write(strTime)
                        file.write(" :- ")
                        say("writing note sir!")
                        file.write(note)
                    else:
                        file.write(note)
                    return f"Note Written Sir"

                elif "show note" in text:
                    pyttsx3.speak("Showing Notes")
                    file = open("proto.txt", "r")
                    k=file.read()
                    print(k)
                    say(k)
                    return k+f"\nNote Opened Sir"


                elif "computer" in text.lower():
                    # use openai key
                    openai.api_key = "sk-proj-RHWcWibL9ykJfFWbu1r8T3BlbkFJO8j81t76AQPDVczGtFLW"
                    query = text.lower().split("computer ")[1]
                    response = openai.Completion.create(
                        model="gpt-3.5-turbo-instruct",
                        prompt=query,
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    print(response.choices[0].text.strip())
                    say(response.choices[0].text.strip())
                    return response.choices[0].text.strip()

                elif " gpt" in text.lower():
                    openai.api_key = "sk-proj-RHWcWibL9ykJfFWbu1r8T3BlbkFJO8j81t76AQPDVczGtFLW"
                    query = text.lower().split("gpt ")[1]
                    conversation.append({"role": "user", "content": query})
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        temperature=0.7,
                        max_tokens=50,
                        messages=conversation
                    )
                    chatGPT_response = response['choices'][0]['message']['content']
                    print(chatGPT_response)
                    say(chatGPT_response)
                    return chatGPT_response

                elif "coder" in text.lower():
                    openai.api_key = "sk-proj-RHWcWibL9ykJfFWbu1r8T3BlbkFJO8j81t76AQPDVczGtFLW"
                    query = text.lower().split("coder")[1]
                    query = query + "Do not respond with additional text. respond in python code only. Do not respond with any explination or greeting whatsoever. Your response in its entirety should only have python code."

                    conversation.append({"role": "user", "content": query})
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=conversation
                    )

                    chatGPT_response = response['choices'][0]['message']['content']
                    print(chatGPT_response)
                    say(chatGPT_response)
                    return chatGPT_response

                else:
                    say('Command not recognized,TRY AGAIN')
                    print("Command not recognized")
                    return f'Command not recognised.TRY AGAIN'

        except sr.UnknownValueError:
                print("Unable to recognize speech")
                return f"Command not recognized,TRY AGAIN"
        except sr.RequestError as e:
                print(f"Error occurred: {e}")
                return f"Error occurred: {e}"

if __name__ == '__main__':

    print('Welcome to PROTO')
    wishMe()
    print("How can I Assist you today?")
    say("How can I Assist you Today?")
    exec(open(r"C:\Users\Tanusri Nukala\PycharmProjects\PROTO2\gui.py").read())




