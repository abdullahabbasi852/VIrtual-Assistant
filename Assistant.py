# -*- coding: utf-8 -*-
from gtts import gTTS
import speech_recognition as sr
import os
import re
import sys
import webbrowser
import wikipedia
import smtplib
import requests
from datetime import datetime
from weather import Weather
import pyttsx3
import random
from tkinter import *


def speak(a = "No Text Assigned"):
    engine = pyttsx3.init()
    engine.say(a)
    engine.runAndWait()

def talkToMe(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def greetings():
    greet = ['hola', 'hello', 'hi', 'Hi', 'hey!','hey']
    r_g = random.choice(greet)
    speak(str(r_g))

def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        r.energy_threshold = 2000
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')

    except sr.UnknownValueError:
        print('Your last command couldn\'t be heard')
        command = myCommand();

    return command


def assistant(command):
    
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        print('Done!')

    elif 'video of' in command:
            reg_ex = re.search('video of (.+)', command)
            if reg_ex:
                domain = reg_ex.group(1)
                url = 'https:www.youtube.com/results?search_query=' + domain
                webbrowser.open(url)
                print('Done!')

    elif 'who is' in command:
          reg_ex = re.search('who is (.+)', command)
          wkpres = wikipedia.summary(command,sentences=2)
          if reg_ex:
              try:
                  engine.say(wkpres)
                  engine.runAndWait()
                  print wkpres
              except wikipedia.summary():
                  print('Not Found!')
                
    elif 'application' in command:
        if 'paint' in command:
            os.system('mspaint')  

        elif 'calculator' in command:                        
            os.system('calc')
        

    
    elif 'open website' in command:
        reg_ex = re.search('open website (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.' + domain + '.com'
            webbrowser.open(url)
            print('Done!')
        else:
            pass
        
    elif 'search' in command:
        reg_ex = re.search('search (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            url = 'https://www.google.com.pk/search?q=' + domain
            webbrowser.open(url)
            print('Done!')
        else:
            pass

    elif 'what\'s up' in command:
        talkToMe('Just doing my thing')
    elif 'joke' in command:
        res = requests.get(
                'https://icanhazdadjoke.com/',
                headers={"Accept":"application/json"}
                )
        if res.status_code == requests.codes.ok:
            talkToMe(str(res.json()['joke']))
            speak(str(res.json()['joke']))
        else:
            talkToMe('oops!I ran out of jokes')
            speak('oops!I ran out of jokes')

    elif 'current time' in command:                                                                        
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            if hour < 12:
                print hour,":",minute,"AM"
                speak(str(hour,":",minute,"AM"))
            if hour == 12:
                hour,":",minute,"PM"
                speak(str(hour,":",minute,"PM"))
            if hour > 12:
                if hour < 18:
                    hour,":",minute,"PM"
                    speak(str(hour,":",minute,"PM"))
                if hour >= 18:
                    hour,":",minute,"AM"
                    speak(str(hour,":",minute,"AM"))
    
    elif 'temperature' or 'current weather in' or 'current temperature in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        reg_ex = re.search('current temperature in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=2f5f6412c3022096d03d549c4dc30ea9").json()
            fd = r['weather'][0]['description']
            t = (r['main']['temp'])-273.15
            send = 'There is '+fd+' in '+city+'\nThe temperature is '+str(t)+'C'
            talkToMe(send)
            speak(send)
        elif reg_ex == 0 or command == 'temperature':
            city = 'karachi'
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=2f5f6412c3022096d03d549c4dc30ea9").json()
            fd = r['weather'][0]['description']
            t = (r['main']['temp'])-273.15
            send = 'There is '+fd+' in '+city+'\nThe temperature is '+str(t)+'C'
            talkToMe(send)
            speak(send)

    elif 'email' or 'gmail' in command:
        a1 = 'Enter Recepient Email:'
        a2 = 'Enter Message:'
        speak(a1)
        email_to = raw_input(a1)
        speak(a2)
        message = raw_input(a2)
        email_user = "abdullahabbasi852@gmail.com"
        a3 = 'Enter Password:'
        speak(a3)
        email_pass = raw_input('Enter Email Password:')
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login(email_user,email_pass)
        server.sendmail(email_user,email_to,message)
        server.close()
        print "Done"

    else:
        talkToMe("I don't what you mean")
    
talkToMe('I am ready for your command')

greetings()
while True:
    assistant(myCommand())
