import speech_recognition as sr
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import os
import subprocess
try:
    os.environ.pop('PYTHONIOENCODING')
except KeyError:
    pass
import pyttsx3
engine = pyttsx3.init()

chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Anukul: {query}\n AI Speech Model: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")


    with open(f"Openai/{''.join(prompt.split('ai')[1:]).strip() }.txt", "w") as f:
        f.write(text)

def say(text):
    engine.say(f"{text}")
    engine.runAndWait()
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold =0.5
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Me"

if __name__ == '__main__':
    print('Welcome to Speech Recognition A.I Model, Anukul')
    say("Welcome to Speech Recognition AI Model, Anukul")
    while True:
        print("Listening...")
        query = takeCommand()

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],
                 ["Abs website", "https://abes.ac.in/"]]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "play music" in query:
            musicPath = "F:/Download/fur-elise-15061.mp3"
            os.system(f"start {musicPath}")

        elif "tell me the time" in query:
            # musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"The time is {hour} hours and {min} minutes")

        # elif "open camera".lower() in query.lower():
        #     os.system(f"start /System/Applications/Camera.app")

        elif "I want to take notes".lower() in query.lower():
            os.system(f"start C:/Windows/system32/notepad")

        elif "Using AI".lower() in query.lower():
            ai(prompt=query)

        elif "Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)





        # say(query)