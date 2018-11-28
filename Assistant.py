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
import pyperclip
import win32com.client
import pyttsx3
import random

#shell = win32com.client.Dispatch("WScript.Shell")


engine = pyttsx3.init()
engine.say('Good morning.')
engine.runAndWait()
engine.say('Hello there!!')
engine.runAndWait()


def talkToMe(audio):
    "speaks audio passed as argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)

def greetings():
    print 'Random'

def myCommand():
    "listens for commands"

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Ready...')
        r.pause_threshold = 1
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
    "if statements for executing commands"

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
        else:
            talkToMe('oops!I ran out of jokes')

    elif 'current time' in command:                                                                        
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            if hour < 12:
                print hour,":",minute,"AM"
                print("Good morning, what can I help you with?")
            if hour == 12:
                hour,":",minute,"PM"
                print("Good day, what can I help you with?")
            if hour > 12:
                if hour < 18:
                    hour,":",minute,"PM"
                    print("Good afternoon, what can I help you with?")
                if hour >= 18:
                    hour,":",minute,"AM"
                    print("Good evening, what can I help you with?")
    
    elif 'current weather in' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            r = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+city+"&APPID=2f5f6412c3022096d03d549c4dc30ea9").json()
            fd = r['weather'][0]['description']
            t = (r['main']['temp'])-273.15
            talkToMe('The Current Weather in '+city+' is '+fd+'\nThe tempeture is '+str(t)+'C')
            engine.say('The Current Weather in '+city+' is '+fd+'\nThe tempeture is '+str(t)+'Celcius')
            engine.runAndWait()

    elif 'email' in command:
        email_to = input('Enter Email:')
        message = input('Enter Message:')
        email_user = 'abdullahabbasi852@gmail.com'
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(email_user,'Concepts05')
        #message = 'python mail'
        server.sendmail(email_user,email_to,message)
        server.quit()
        print "Done"

talkToMe('I am ready for your command')


while True:
    assistant(myCommand())
