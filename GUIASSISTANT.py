from os import path
from tkinter import font

ai_name = 'ALICIA'.lower()
EXIT_COMMANDS = ['bye', 'exit', 'quit', 'shut down', 'shutdown']

rec_email, rec_phoneno = "", ""
WAEMEntry = None

avatarChoosen = 0
choosedAvtrImage = None

botChatTextBg = "#0f0931"
botChatText = "white"
userChatTextBg = "#4da8da"



chatBgColor = '#12232e'   
background = '#203647'
textColor = 'white'
AITaskStatusLblBG = '#203647'
KCS_IMG = 1  
voice_id = 0  # 0 for female, 1 for male
ass_volume = 1  # max volume
ass_voiceRate = 200  # normal voice rate

####################### IMPORTING MODULES ##############
""" User Created Modules """
try:
    import normalChat
    import math_function
    import appControl
    import game
    import webScrapping
    from userHandler import UserData
    import timer
    from FACE_UNLOCKER import clickPhoto, viewPhoto
    import dictionary
    from normalChat import DateTime
    import ToDo
    import fileHandler
except Exception as e:
    raise e

""" System Modules """
try:
    import os
    import qrcode
    import datetime
    import speech_recognition as sr
    import pyttsx3
    import webbrowser
    import requests
    import time
    import instadownloader
    from tkinter import *
    from tkinter import ttk
    from tkinter import messagebox
    from tkinter import colorchooser
    from PIL import Image, ImageTk
    from requests import get
    import cv2
    from time import sleep
    from threading import Thread
    from requests import get
    import urllib.request
    import numpy as np
    import PyPDF2
    import MyAlarm
    from twilio.rest import Client
    from pywikihow import search_wikihow
    import wikipedia
    import psutil
    import speedtest
except Exception as e:
    print(e)

########################################## LOGIN CHECK ##############################################
try:
    user = UserData()
    user.extractData()
    ownerName = user.getName().split()[0]
    ownerDesignation = "Sir"
    if user.getGender() == "Female":
        ownerDesignation = "Ma'am"
    ownerPhoto = user.getUserPhoto()
except Exception as e:
    print("You're not Registered Yet !\nRun ALICIA.py file to register your face.")
    raise SystemExit


########################################## BOOT UP WINDOW ###########################################
def ChangeSettings(write=False):
    import pickle
    global background, textColor, chatBgColor, voice_id, ass_volume, ass_voiceRate, AITaskStatusLblBG, KCS_IMG, botChatTextBg, botChatText, userChatTextBg
    setting = {'background': background,
               'textColor': textColor,
               'chatBgColor': chatBgColor,
               'AITaskStatusLblBG': AITaskStatusLblBG,
               'KCS_IMG': KCS_IMG,
               'botChatText': botChatText,
               'botChatTextBg': botChatTextBg,
               'userChatTextBg': userChatTextBg,
               'voice_id': voice_id,
               'ass_volume': ass_volume,
               'ass_voiceRate': ass_voiceRate
               }
    if write:
        with open('userData/settings.pck', 'wb') as file:
            pickle.dump(setting, file)
        return
    try:
        with open('userData/settings.pck', 'rb') as file:
            loadSettings = pickle.load(file)
            background = loadSettings['background']
            textColor = loadSettings['textColor']
            chatBgColor = loadSettings['chatBgColor']
            AITaskStatusLblBG = loadSettings['AITaskStatusLblBG']
            KCS_IMG = loadSettings['KCS_IMG']
            botChatText = loadSettings['botChatText']
            botChatTextBg = loadSettings['botChatTextBg']
            userChatTextBg = loadSettings['userChatTextBg']
            voice_id = loadSettings['voice_id']
            ass_volume = loadSettings['ass_volume']
            ass_voiceRate = loadSettings['ass_voiceRate']
    except Exception as e:
        pass


if os.path.exists('userData/settings.pck') == False:
    ChangeSettings(True)


def getChatColor():
    global chatBgColor
    chatBgColor = myColor[1]
    colorbar['bg'] = chatBgColor
    chat_frame['bg'] = chatBgColor
    root1['bg'] = chatBgColor


def changeTheme():
    global background, textColor, AITaskStatusLblBG, KCS_IMG, botChatText, botChatTextBg, userChatTextBg, chatBgColor
    if themeValue.get() == 1:
        background, textColor, AITaskStatusLblBG, KCS_IMG = "#203647", "white", "#203647", 1
        cbl['image'] = cblDarkImg
        kbBtn['image'] = kbphDark
        settingBtn['image'] = sphDark
        AITaskStatusLbl['bg'] = AITaskStatusLblBG
        botChatText, botChatTextBg, userChatTextBg = "white", "#0f0931", "#4da8da"
        chatBgColor = "#12232e"
        colorbar['bg'] = chatBgColor
    else:
        background, textColor, AITaskStatusLblBG, KCS_IMG = "#F6FAFB", "#303E54", "#14A769", 0
        cbl['image'] = cblLightImg
        kbBtn['image'] = kbphLight
        settingBtn['image'] = sphLight
        AITaskStatusLbl['bg'] = AITaskStatusLblBG
        botChatText, botChatTextBg, userChatTextBg = "#494949", "#0f0931", "#23AE79"
        chatBgColor = "#F6FAFB"
        colorbar['bg'] = '#E8EBEF'

    root['bg'], root2['bg'] = background, background
    settingsFrame['bg'] = background
    settingsLbl['fg'], userPhoto['fg'], userName['fg'], assLbl['fg'], voiceRateLbl['fg'], volumeLbl['fg'], themeLbl[
        'fg'], chooseChatLbl['fg'] = textColor, textColor, textColor, textColor, textColor, textColor, textColor, textColor
    settingsLbl['bg'], userPhoto['bg'], userName['bg'], assLbl['bg'], voiceRateLbl['bg'], volumeLbl['bg'], themeLbl[
        'bg'], chooseChatLbl['bg'] = background, background, background, background, background, background, background, background
    s.configure('Wild.TRadiobutton', background=background,
                foreground=textColor)
    volumeBar['bg'], volumeBar['fg'], volumeBar['highlightbackground'] = background, textColor, background
    chat_frame['bg'], root1['bg'] = chatBgColor, chatBgColor
    userPhoto['activebackground'] = background
    ChangeSettings(True)


def changeVoice(e):
    global voice_id
    voice_id = 0
    if assVoiceOption.get() == 'Male':
        voice_id = 1
    engine.setProperty('voice', voices[1].id)
    ChangeSettings(True)


def changeVolume(e):
    global ass_volume
    ass_volume = volumeBar.get() / 100
    engine.setProperty('volume', ass_volume)
    ChangeSettings(True)


def changeVoiceRate(e):
    global ass_voiceRate
    temp = voiceOption.get()
    if temp == 'Very Low':
        ass_voiceRate = 100
    elif temp == 'Low':
        ass_voiceRate = 150
    elif temp == 'Fast':
        ass_voiceRate = 250
    elif temp == 'Very Fast':
        ass_voiceRate = 300
    else:
        ass_voiceRate = 200
    print(ass_voiceRate)
    engine.setProperty('rate', ass_voiceRate)
    ChangeSettings(True)


ChangeSettings()

############################################ SET UP VOICE ###########################################
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # male
    engine.setProperty('volume', ass_volume)
except Exception as e:
    print(e)


####################################### SET UP TEXT TO SPEECH #######################################
def speak(text, display=False, icon=False):
    AITaskStatusLbl['text'] = 'Speaking...'
    if icon:
        Label(chat_frame, image=botIcon, bg=chatBgColor).pack(
            anchor='w', pady=0)
    if display:
        attachTOframe(text, True)
    print('\n'+ai_name.upper()+': '+text)
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        print("Try not to type more...")

####################################### SET UP SPEECH TO TEXT #######################################

def demo():
    speak("Hello I am Alicia your AI Virtual Assistant. Please Tell me how may I assist you", True, True)

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good Morning", True, True)
    elif hour>=12 and hour<18:
        speak("Good Afternoon", True, True)

    else:
        speak("Good Evening", True, True)

def verify():
    speak("Authentication Successfull !!!. The user has been verified", True, True)

def wishtime():
    dt = DateTime()
    result = "It's: " + dt.currentTime()
    speak(result, True, True)
    return

def pdf_reader():
    book = open('demo.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak(f"Total number of pages in this book is {pages} ", True, True)
    speak("Please enter the page number I have to read", True, True)
    pg = int(input("Please enter the page number: "))
    page = pdfReader.getPage(pg)
    text = page.extractText()
    speak(text)


def record(clearChat=True, iconDisplay=True):
    print('\nListening...')
    AITaskStatusLbl['text'] = 'Listening...'
    r = sr.Recognizer()
    r.dynamic_energy_threshold = False
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        said = ""
        try:
            AITaskStatusLbl['text'] = 'Processing...'
            said = r.recognize_google(audio)
            print(f"\nUser said: {said}")
            if clearChat:
                clearChatScreen()
            if iconDisplay:
                Label(chat_frame, image=userIcon, bg=chatBgColor).pack(
                    anchor='e', pady=0)
            attachTOframe(said)
        except Exception as e:
            print(e)
            # speak("I didn't get it, Say that again please...")
            if "connection failed" in str(e):
                speak("Your System is Offline...", True, True)
            return 'None'
    return said.lower()


def voiceMedium():
    verify()
    wish()
    wishtime()
    demo()
    while True:
        query = record()
        if query == 'None':
            continue
        if isContain(query, EXIT_COMMANDS):
            os.system("taskkill /f /im ALICIA.exe")
            speak("Shutting down the System. Good Bye!!", True, True)
            break
        else:
            main(query.lower())
    appControl.Win_Opt('close')



def keyboardInput(e):
    user_input = UserField.get().lower()
    if user_input != "":
        clearChatScreen()
        if isContain(user_input, EXIT_COMMANDS):
            speak("Shutting down the System. Good Bye!!", True, True)
        else:
            Label(chat_frame, image=userIcon, bg=chatBgColor).pack(
                anchor='e', pady=0)
            attachTOframe(user_input.capitalize())
            Thread(target=main, args=(user_input,)).start()
        UserField.delete(0, END)

###################################### TASK/COMMAND HANDLER #########################################


def isContain(txt, lst):
    for word in lst:
        if word in txt:
            return True
    return False


def main(text):
    
    if "project" in text:
        if isContain(text, ['make', 'create']):
            speak("What do you want to give the project name ?", True, True)
            projectName = record(False, False)
            speak(fileHandler.CreateHTMLProject(
                projectName.capitalize()), True)
            return

    if "create" in text and "file" in text:
        speak(fileHandler.createFile(text), True, True)
        return

    if "translate" in text:
        speak("What do you want to translate?", True, True)
        sentence = record(False, False)
        speak("Which langauage to translate ?", True)
        langauage = record(False, False)
        result = normalChat.lang_translate(sentence, langauage)
        if result == "None":
            speak("This langauage doesn't exists")
        else:
            speak(f"In {langauage.capitalize()} you would say:", True)
            if langauage == "hindi":
                attachTOframe(result.text, True)
                speak(result.pronunciation)
            else:
                speak(result.text, True)
        return

    #Advanced level assistant commands of ALICIA   
    if 'close notepad' in text:
                speak("Closing notepad", True, True)
                os.system("taskkill /f /im notepad.exe")
    
    # if 'shutdown the system' in text:
    #             speak("closing system", True, True)
    #             os.system("shutdown /s /t 5")
            
    if 'sleep the system' in text:
                speak("sleeping system", True, True)
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    if 'command prompt' in text:
                speak("Opening command prompt", True, True)
                os.system("start cmd")

    if 'camera' in text:
                speak("Opening camera", True, True)
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break

                cap.release()
                cv2.destroyAllWindows()
            
            
    if 'ip address' in text:
                speak("Getting ip address", True, True)
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                speak(f"your IP address is {ip}")

    if 'generate qr code' in text:
                speak("Say Link to the Website...", True, True)
                audio1 =  record().lower()
                # try:
                #     text1 = record().lower(audio1)
                #     speak('You said :{}'.format(text1), True, True)
                # except:
                #     speak('Cannot Listen', True, True)
                speak('What should be file name...', True, True)
                
                audio = record().lower()
                # try:
                #     text = record().lower()
                #     print('Saving as :{}'.format(text),'.png')
                # except:
                #     speak('Cannot Listen', True, True)
                img = qrcode.make('https://'+audio1+'/in/') #Accepts the Users URL 
                img.save(audio+'.png') #Creates image in the form of QR code using URL
                speak('QR Code sucessfully generated and saved in your main file...', True, True)
            


    if 'virtual paint' in text:
                speak("Opening virtual paint", True, True)
                codePath = "AirCanvas2.exe"
                os.startfile(codePath)
                return
    
    if 'snake game' in text:
                speak("Opening Snake Game", True, True)
                codePath = "SnakeGame.exe"
                os.startfile(codePath)
                return
    
    if 'quiz game' in text:
                speak("Opening Quiz Game", True, True)
                codePath = "QuizGame.exe"
                os.startfile(codePath)
                return
    
    if 'where I am' in text or 'where we are' in text:
                speak("Wait, let me check", True, True)
                try:
                    ipAdd = requests.get('https://api.ipify.org').text
                    print(ipAdd)
                    url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    city = geo_data['city']
                    country = geo_data['country']
                    print(f"I am not sure, but I think we are in {city} city of {country} country")
                    speak(f"I am not sure, but I think we are in {city} city of {country} country", True, True)
                except Exception as e:
                    speak("Sorry, due to network issue I am not able to find your location")
                    pass
            
    if 'Instagram profile' in text or 'profile on instagram' in text:
                speak("Please enter the username correctly.", True, True)
                name = input("Enter username here:")
                webbrowser.open(f"www.instagram.com/{name}")
                speak("Here is the profile of the user {name}", True, True)
                time.sleep(5)
                speak("Would you like to download the profile picture of this account.", True, True)
                condition = record().lower()
                if "yes" in condition:
                    mod = instadownloader.InstaDownloader()
                    mod.download_profile(name, profile_pic_only=True)
                    speak("I am done, profile picture is saved in our main folder, now I am ready for next command", True, True)
                else:
                    pass
    
    if 'read pdf' in text:
                pdf_reader()

    if 'hide all files' in text or 'hide this folder' in text or 'visible for everyone' in text:
                speak("Please tell me you want to hide this folder or make it visible for everyone", True, True)
                condition = record().lower()
                if "hide" in condition:
                    os.system("attrib +h /s /d")
                    speak("All the files in this folder are now hidden", True, True)
                
                elif "visible" in condition:
                    os.system("attrib -h /s /d")
                    speak("All the files in this folder are now visible for everyone", True, True)
                
                elif "leave it" in condition or "leave for now" in condition:
                    speak("Ok")
    
    if 'activate how to do mode' in text:
                speak("How to do mode is activated", True, True)
                while True:
                    speak("Please tell me what you want to know", True, True)
                    how = record().lower()
                    try:
                        if "exit" in how or "close" in how:
                            speak("Ok, how to do mode is closed", True, True)
                            break
                        else:
                            max_results = 1
                            how_to = search_wikihow(how, max_results)
                            assert len(how_to) == 1
                            how_to[0].print()
                            speak(how_to[0].summary, True, True)

                    except Exception as e:
                        speak("Sorry, I am not able to find this", True, True)
            
    if 'how much power left' in text or 'check battery status' in text:

                battery = psutil.sensors_battery()
                percentage = battery.percent
                speak(f"Our system has {percentage} percent battery", True, True)
                if percentage >= 75:
                    speak("We have enough power to continue our work", True, True)
                elif percentage >= 40 and percentage <= 75:
                    speak("We should connect our system to charging point to charge our battery", True, True)
                elif percentage >=15 and percentage <= 30:
                    speak("We don't have enough power to work, please connect to charging", True, True)
                elif percentage <= 15:
                    speak("We have very low power, please connect to charging. The system will shutdown very soon", True, True)
    
    if 'internet speed' in text:

                st = speedtest.Speedtest()
                dl = st.download()
                up = st.upload()
                speak(f"We have {dl} bit per second downloading and {up} bit per second uploading speed", True, True)

                # try:
                #     comnet = os.system('cmd /k "speedtest"')
                #     speak(f"{comnet}", True, True)



                # except:
                #     speak("There is no Internet Connected to your system", True, True)

    
    if 'send sms' in text:
                # Download the helper library from https://www.twilio.com/docs/python/install
                speak("What should I say", True, True)
                msz = record().lower()

                account_sid = 'AC7757f19be15197d51377d4ee363cfd1b'
                auth_token = '9b47929b5bd1545aebbf322767976f9c'
                client = Client(account_sid, auth_token)

                message = client.messages \
                    .create(
                        body = msz,
                        from_='+19123781897',
                        to='+919324855066'
                        )
                
                speak("Your message has been sent", True, True)
                print(message.sid)
            
    if 'call' in text:
                # Download the helper library from https://www.twilio.com/docs/python/install
                speak("What should I say", True, True)
                msz = record().lower()

                account_sid = 'AC7757f19be15197d51377d4ee363cfd1b'
                auth_token = '9b47929b5bd1545aebbf322767976f9c'
                client = Client(account_sid, auth_token)

                message = client.calls \
                    .create(
                        twiml = '<Response><Say>this is a testing call from Alicia virtual assistant you can send any message through a call using Alicia.</Say></Response>',
                        from_='+19123781897',
                        to='+919324855066'
                        )
                
                speak("Your call has been sent", True, True)
                print(message.sid)
    
    if 'alarm' in text:
                speak("Please tell me the time to set alarm. for example, set alarm to 5 30 AM", True, True)
                tt = record().lower()
                tt = tt.replace("set alarm to ", "")
                tt = tt.replace(".","")
                tt = tt.upper()
                MyAlarm.alarm(tt)
            
    if 'mobile server' in text:
                URL = "http://192.168.0.107:8080/shot.jpg"
                while True:
                    img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                    img = cv2.imdecode(img_arr,-1)
                    cv2.imshow('Alicia Webcam',img)
                    q = cv2.waitKey(1)
                    if q == ord("q"):
                        break;
                
                cv2.destroyAllWindows()
      
    if 'open PHCET college website' in text:
                speak("Opening your college website", True, True)
                webbrowser.open("https://phcet.ac.in/")
        
    if 'open my college website' in text:
                speak("Opening your college website", True, True)
                webbrowser.open("https://phcet.ac.in/")
        
    if 'open student portal' in text:
                speak("Opening student portal, Please pay your college fees Dues.", True, True)
                webbrowser.open("https://phcetstudentportal.mes.ac.in/")
    
    if 'youtube kholo' in text:
                speak("Youtube khul rhaa hai rukiyee zaraa", True, True)
                webbrowser.open("https://www.youtube.com/")
            
    if 'who are you' in text:
                speak("Myself Alicia, World's most advanced AI, I love to help people virtually, I can do anything for you, if you want to know about AI have a look at this", True, True)
                webbrowser.open("https://www.ibm.com/in-en/cloud/learn/what-is-artificial-intelligence")

    if 'go to hell' in text:
                speak("You go to hell, why should I, I am here for your assistance, you should respect me", True, True)

    if 'i am bored now' in text:
                speak("Don't be, I am here for you, here are some entertainmnet for you", True, True)
                webbrowser.open("https://www.netflix.com/browse")

    if 'hello Alicia' in text:
                speak("Hello. please tell me how may I assist you", True, True)

    if 'talk with me in hindi' in text:
                speak("Namaste, mai kya kar sakti hu aapke keliye", True, True)

    if 'hey Alicia' in text:
                speak("Hello, what can I do for you", True, True)

    if 'hi Alicia' in text:
                speak("Hello, what can I do for you", True, True)
    
    if 'tell me something about yourself' in text:
                speak("Myself Alicia, World's most advanced AI, I love to help people virtually, I can do anything for you, if you want to know about AI have a look at this.", True, True)
                webbrowser.open("https://www.ibm.com/in-en/cloud/learn/what-is-artificial-intelligence")
            
    if 'kaun ho tum' in text:
                speak("Mera naam Alicia hai, mujhe logo ki help karna acchaa lagtaa hai, mere baare mein jaanane ke liye AI ke baare mein  jaane", True, True)
                webbrowser.open("https://www.ibm.com/in-en/cloud/learn/what-is-artificial-intelligence")


    if 'list' in text:
        if isContain(text, ['add', 'create', 'make']):
            speak("What do you want to add?", True, True)
            item = record(False, False)
            ToDo.toDoList(item)
            speak("Alright, I added to your list", True)
            return
        if isContain(text, ['show', 'my list']):
            items = ToDo.showtoDoList()
            if len(items) == 1:
                speak(items[0], True, True)
                return
            attachTOframe('\n'.join(items), True)
            speak(items[0])
            return

    if isContain(text, ['battery', 'system info']):
        result = appControl.OSHandler(text)
        if len(result) == 2:
            speak(result[0], True, True)
            attachTOframe(result[1], True)
        else:
            speak(result, True, True)
        return
    
    if isContain(text, ['alexa', 'siri', 'cortana', 'google assistant']):
        speak("Yes I like her. She is an inspiration for me but I will be much better than her", True, True)
    
    if isContain(text, ['idiot', 'stupid', 'gadhi', 'pagal', 'ullu',]):
        speak("See I am in my testing mode. So don't ask such questions which are above my capability.", True, True)
    
    if isContain(text, ['lonely', 'sad', 'help', 'tension', 'depression' 'depressed', 'sorrow']):
        speak("Don't worry. I am always with you. I will always be there for your assistance", True, True)
    
    if isContain(text, ['upset', 'help', 'laugh', 'work properly' 'boring', 'slow']):
        speak("I will try my best to never let you down.", True, True)
    

    


    if isContain(text, ['meaning', 'dictionary', 'definition', 'define']):
        result = dictionary.translate(text)
        speak(result[0], True, True)
        if result[1] == '':
            return
        speak(result[1], True)
        return

    if 'selfie' in text or ('click' in text and 'photo' in text):
        speak("Sure "+ownerDesignation+"...", True, True)
        clickPhoto()
        speak('Do you want to view your clicked photo?', True)
        query = record(False)
        if isContain(query, ['yes', 'sure', 'yeah', 'show me']):
            Thread(target=viewPhoto).start()
            speak("Ok, here you go...", True, True)
        else:
            speak("No Problem "+ownerDesignation, True, True)
        return

    if 'volume' in text:
        appControl.volumeControl(text)
        Label(chat_frame, image=botIcon, bg=chatBgColor).pack(
            anchor='w', pady=0)
        attachTOframe('Volume Settings Changed', True)
        return

    if isContain(text, ['timer', 'countdown']):
        Thread(target=timer.startTimer, args=(text,)).start()
        speak('Ok, Timer Started!', True, True)
        return

    if 'whatsapp' in text:
        speak("Sure "+ownerDesignation+"...", True, True)
        speak('Whom do you want to send the message?', True)
        WAEMPOPUP("WhatsApp", "Phone Number")
        attachTOframe(rec_phoneno)
        speak('What is the message?', True)
        message = record(False, False)
        Thread(target=webScrapping.sendWhatsapp,
               args=(rec_phoneno, message,)).start()
        speak("Message is on the way. Do not move away from the screen.")
        attachTOframe("Message Sent", True)
        return

    if 'vs code' in text:
        speak("opening vs code")
        codePath = "C:\\Users\\Rishabh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)
        return

    if 'my files' in text:
        speak("opening your files")
        codePath = "D:\Rajat"
        os.startfile(codePath)
        return

    if 'virtual mouse' in text:
        speak("Opening virtual mouse", True, True)
        codePath = "handTracker2.exe"
        os.startfile(codePath)
        return
    
    if 'virtual keyboard' in text:
        speak("Opening virtual keyboard", True, True)
        codePath = "onscreenkeyboard.exe"
        os.startfile(codePath)
        return

    if 'email' in text:
        speak('Whom do you want to send the email?', True, True)
        WAEMPOPUP("Email", "E-mail Address")
        attachTOframe(rec_email)
        speak('What is the Subject?', True)
        subject = record(False, False)
        speak('What message you want to send ?', True)
        message = record(False, False)
        Thread(target=webScrapping.email, args=(
            rec_email, message, subject,)).start()
        speak('Email has been Sent', True)
        return

    if isContain(text, ['covid', 'virus']):
        result = webScrapping.covid(text)
        if 'str' in str(type(result)):
            speak(result, True, True)
            return
        speak(result[0], True, True)
        result = '\n'.join(result[1])
        attachTOframe(result, True)
        return

    if isContain(text, ['youtube', 'video', 'play','play youtube video']):
        speak("Ok "+ownerDesignation+", here a video for you...", True, True)
        try:
            speak(webScrapping.youtube(text), True)
        except Exception as e:
            speak("Desired Result Not Found", True)
        return

    if isContain(text, ['search', 'image']):
        if 'image' in text and 'show' in text:
            Thread(target=showImages, args=(text,)).start()
            speak('Here are the images...', True, True)
            return
        speak(webScrapping.googleSearch(text), True, True)
        return

    if isContain(text, ['map', 'direction']):
        if "direction" in text:
            speak('What is your starting location?', True, True)
            startingPoint = record(False, False)
            speak("Ok "+ownerDesignation+", Where you want to go?", True)
            destinationPoint = record(False, False)
            speak("Ok "+ownerDesignation+", Getting Directions...", True)
            try:
                distance = webScrapping.giveDirections(
                    startingPoint, destinationPoint)
                speak('You have to cover a distance of ' + distance, True)
            except:
                speak("I think location is not proper, Try Again!")
        else:
            webScrapping.maps(text)
            speak('Here you go...', True, True)
        return

    if isContain(text, ['factorial', 'log', 'value of', 'math', ' + ', ' - ', ' x ', '/', '%', 'multiply', 'into', 'divided by', 'modulus', 'binary', 'hexadecimal', 'octal', 'shift', 'sin ', 'cos ', 'tan ']):
        try:
            speak(('Result is: ' + math_function.perform(text)), True, True)
        except Exception as e:
            return
        return

    if "joke" in text:
        speak('Here is a joke...', True, True)
        speak(webScrapping.jokes(), True)
        return

    if isContain(text, ['news']):
        speak('Getting the latest news...', True, True)
        headlines, headlineLinks = webScrapping.latestNews(2)
        for head in headlines:
            speak(head, True)
        speak('Do you want to read the full news?', True)
        text = record(False, False)
        if isContain(text, ["no", "don't"]):
            speak("No Problem "+ownerDesignation, True)
        else:
            speak("Ok "+ownerDesignation+", Opening browser...", True)
            webScrapping.openWebsite('https://indianexpress.com/latest-news/')
            speak("You can now read the full news from this website.")
        return

    if isContain(text, ['weather']):
        data = webScrapping.weather()
        speak('', False, True)
        showSingleImage("weather", data[:-1])
        speak(data[-1])
        return

    if isContain(text, ['screenshot']):
        Thread(target=appControl.Win_Opt, args=('screenshot',)).start()
        speak("Screen Shot Taken", True, True)
        return

    if isContain(text, ['window', 'close that']):
        appControl.Win_Opt(text)
        return

    if isContain(text, ['tab']):
        appControl.Tab_Opt(text)
        return

    if isContain(text, ['setting']):
        raise_frame(root2)
        clearChatScreen()
        return

    if isContain(text, ['open', 'type', 'save', 'delete', 'select', 'press enter']):
        appControl.System_Opt(text)
        return

    if isContain(text, ['wiki', 'who is']):
        Thread(target=webScrapping.downloadImage, args=(text, 1,)).start()
        speak('Searching...', True, True)
        result = webScrapping.wikiResult(text)
        showSingleImage('wiki')
        speak(result, True)
        return

    if isContain(text, ['games']):
        speak("Which game do you want to play?", True, True)
        attachTOframe(game.showGames(), True)
        text = record(False)
        if text == "None":
            speak("Didn't understand what you say?", True, True)
            return
        if 'online' in text:
            speak("Ok "+ownerDesignation +
                  ", Let's play some online games", True, True)
            webScrapping.openWebsite('https://www.agame.com/games/mini-games/')
            return
        if isContain(text, ["don't", "no", "cancel", "back", "never", "quit"]):
            speak("No Problem "+ownerDesignation +
                  ", We'll play next time.", True, True)
        else:
            speak("Ok "+ownerDesignation+", Let's Play " + text, True, True)
            os.system(f"python -c \"import game; game.play('{text}')\"")
        return
    
    if isContain(text, ['coin', 'dice', 'die']):
        if "toss" in text or "roll" in text or "flip" in text:
            speak("Ok "+ownerDesignation, True, True)
            result = game.play(text)
            if "Head" in result:
                showSingleImage('head')
            elif "Tail" in result:
                showSingleImage('tail')
            else:
                showSingleImage(result[-1])
            speak(result)
            return


    if isContain(text, ['time', 'date']):
        speak(normalChat.chat(text), True, True)
        return

    if 'my name' in text:
        speak('Your name is, ' + ownerName, True, True)
        return

    if isContain(text, ['voice']):
        global voice_id
        try:
            if 'female' in text:
                voice_id = 0
            elif 'male' in text:
                voice_id = 1
            else:
                if voice_id == 0:
                    voice_id = 1
                else:
                    voice_id = 0
            engine.setProperty('voice', voices[voice_id].id)
            ChangeSettings(True)
            speak("Hello "+ownerDesignation +
                  ", I have changed my voice. How may I help you?", True, True)
            assVoiceOption.current(voice_id)
        except Exception as e:
            print(e)
        return

    if isContain(text, ['morning', 'evening', 'noon']) and 'good' in text:
        speak(normalChat.chat("good"), True, True)
        return

    result = normalChat.reply(text)
    if result != "None":
        speak(result, True, True)
    else:
        speak("Here's what I found on the web... ", True, True)
        webScrapping.googleSearch(text)


##################################### DELETE USER ACCOUNT #########################################
def deleteUserData():
    result = messagebox.askquestion(
        'Alert', 'Are you sure you want to delete your Face Data ?')
    if result == 'no':
        return
    messagebox.showinfo(
        'Clear Face Data', 'Your face has been cleared\nRegister your face again to use.')
    import shutil
    shutil.rmtree('userData')
    root.destroy()


#####################
####### GUI #########
#####################

############ ATTACHING BOT/USER CHAT ON CHAT SCREEN ###########


def attachTOframe(text, bot=False):
    if bot:
        botchat = Label(chat_frame, text=text, bg=botChatTextBg, fg=botChatText,
                        justify=LEFT, wraplength=250, font=('Montserrat', 12, 'bold'))
        botchat.pack(anchor='w', ipadx=5, ipady=5, pady=5)
    else:
        userchat = Label(chat_frame, text=text, bg=userChatTextBg, fg='white',
                         justify=RIGHT, wraplength=250, font=('Montserrat', 12, 'bold'))
        userchat.pack(anchor='e', ipadx=2, ipady=2, pady=5)


def clearChatScreen():
    for wid in chat_frame.winfo_children():
        wid.destroy()


### SWITCHING BETWEEN FRAMES ###
def raise_frame(frame):
    frame.tkraise()
    clearChatScreen()

################# SHOWING DOWNLOADED IMAGES ###############
img0, img1, img2, img3, img4 = None, None, None, None, None


def showSingleImage(type, data=None):
    global img0, img1, img2, img3, img4
    try:
        img0 = ImageTk.PhotoImage(Image.open(
            'Downloads/0.jpg').resize((90, 110), Image.ANTIALIAS))
    except:
        pass
    img1 = ImageTk.PhotoImage(Image.open(
        'extrafiles/images/heads.jpg').resize((220, 200), Image.ANTIALIAS))
    img2 = ImageTk.PhotoImage(Image.open(
        'extrafiles/images/tails.jpg').resize((220, 200), Image.ANTIALIAS))
    img4 = ImageTk.PhotoImage(Image.open('extrafiles/images/WeatherImage.png'))

    if type == "weather":
        weather = Frame(chat_frame)
        weather.pack(anchor='w')
        Label(weather, image=img4, bg=chatBgColor).pack()
        Label(weather, text=data[0], font=(
            'Arial Bold', 45), fg='white', bg='#3F48CC').place(x=65, y=45)
        Label(weather, text=data[1], font=('Montserrat', 15),
              fg='white', bg='#3F48CC').place(x=78, y=110)
        Label(weather, text=data[2], font=('Montserrat', 10),
              fg='white', bg='#3F48CC').place(x=78, y=140)
        Label(weather, text=data[3], font=('Arial Bold', 12),
              fg='white', bg='#3F48CC').place(x=60, y=160)

    elif type == "wiki":
        Label(chat_frame, image=img0, bg='#EAEAEA').pack(anchor='w')
    elif type == "head":
        Label(chat_frame, image=img1, bg='#EAEAEA').pack(anchor='w')
    elif type == "tail":
        Label(chat_frame, image=img2, bg='#EAEAEA').pack(anchor='w')
    else:
        img3 = ImageTk.PhotoImage(Image.open(
            'extrafiles/images/dice/'+type+'.jpg').resize((200, 200), Image.ANTIALIAS))
        Label(chat_frame, image=img3, bg='#EAEAEA').pack(anchor='w')


def showImages(query):
    global img0, img1, img2, img3
    webScrapping.downloadImage(query)
    w, h = 150, 110
    # Showing Images
    imageContainer = Frame(chat_frame, bg='#EAEAEA')
    imageContainer.pack(anchor='w')
    # loading images
    img0 = ImageTk.PhotoImage(Image.open(
        'Downloads/0.jpg').resize((w, h), Image.ANTIALIAS))
    img1 = ImageTk.PhotoImage(Image.open(
        'Downloads/1.jpg').resize((w, h), Image.ANTIALIAS))
    img2 = ImageTk.PhotoImage(Image.open(
        'Downloads/2.jpg').resize((w, h), Image.ANTIALIAS))
    img3 = ImageTk.PhotoImage(Image.open(
        'Downloads/3.jpg').resize((w, h), Image.ANTIALIAS))
    # Displaying
    Label(imageContainer, image=img0, bg='#EAEAEA').grid(row=0, column=0)
    Label(imageContainer, image=img1, bg='#EAEAEA').grid(row=0, column=1)
    Label(imageContainer, image=img2, bg='#EAEAEA').grid(row=1, column=0)
    Label(imageContainer, image=img3, bg='#EAEAEA').grid(row=1, column=1)



############################# WAEM - WhatsApp Email ##################################
def sendWAEM():
    global rec_phoneno, rec_email
    data = WAEMEntry.get()
    rec_email, rec_phoneno = data, data
    WAEMEntry.delete(0, END)
    appControl.Win_Opt('close')


def send(e):
    sendWAEM()


def WAEMPOPUP(Service='None', rec='Reciever'):
    global WAEMEntry
    PopUProot = Tk()
    PopUProot.title(f'{Service} Service')
    PopUProot.configure(bg='white')

    if Service == "WhatsApp":
        PopUProot.iconbitmap("extrafiles/images/whatsapp.ico")
    else:
        PopUProot.iconbitmap("extrafiles/images/email.ico")
    w_width, w_height = 410, 200
    s_width, s_height = PopUProot.winfo_screenwidth(), PopUProot.winfo_screenheight()
    x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
    # center location of the screen
    PopUProot.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y-30))
    Label(PopUProot, text=f'Reciever {rec}', font=(
        'Arial', 16), bg='white').pack(pady=(20, 10))
    WAEMEntry = Entry(PopUProot, bd=10, relief=FLAT, font=(
        'Arial', 12), justify='center', bg='#DCDCDC', width=30)
    WAEMEntry.pack()
    WAEMEntry.focus()

    SendBtn = Button(PopUProot, text='Send', font=('Arial', 12),
                     relief=FLAT, bg='#14A769', fg='white', command=sendWAEM)
    SendBtn.pack(pady=20, ipadx=10)
    PopUProot.bind('<Return>', send)
    PopUProot.mainloop()




######################## CHANGING CHAT BACKGROUND COLOR #########################
def getChatColor():
    global chatBgColor
    myColor = colorchooser.askcolor()
    if myColor[1] is None:
        return
    chatBgColor = myColor[1]
    colorbar['bg'] = chatBgColor
    chat_frame['bg'] = chatBgColor
    root1['bg'] = chatBgColor
    ChangeSettings(True)

chatMode = 1

def changeChatMode():
    global chatMode
    if chatMode == 1:
        # appControl.volumeControl('mute')
        VoiceModeFrame.pack_forget()
        TextModeFrame.pack(fill=BOTH)
        UserField.focus()
        chatMode = 0
    else:
        # appControl.volumeControl('full')
        TextModeFrame.pack_forget()
        VoiceModeFrame.pack(fill=BOTH)
        root.focus()
        chatMode = 1

############################################## GUI #############################################
def onhover(e):
    userPhoto['image'] = chngPh


def onleave(e):
    userPhoto['image'] = userProfileImg


def UpdateIMAGE():
    global ownerPhoto, userProfileImg, userIcon

    os.system('python ChooseAvatarPIC.py')
    u = UserData()
    u.extractData()
    ownerPhoto = u.getUserPhoto()
    userProfileImg = ImageTk.PhotoImage(Image.open(
        "extrafiles/images/avatars/a"+str(ownerPhoto)+".png").resize((120, 120)))

    userPhoto['image'] = userProfileImg
    userIcon = PhotoImage(
        file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")


def SelectAvatar():
    Thread(target=UpdateIMAGE).start()

#####################################  MAIN GUI ####################################################


if __name__ == '__main__':
    root = Tk()
    root.title('ALICIA')
    w_width, w_height = 400, 650
    s_width, s_height = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = (s_width/2)-(w_width/2), (s_height/2)-(w_height/2)
    # center location of the screen
    root.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y-30))
    root.configure(bg=background)
    # root.resizable(width=False, height=False)
    root.pack_propagate(0)

    root1 = Frame(root, bg=chatBgColor)
    root2 = Frame(root, bg=background)
    root3 = Frame(root, bg=background)

    for f in (root1, root2, root3):
        f.grid(row=0, column=0, sticky='news')




    ################################
    ########  CHAT SCREEN  #########
    ################################

    # Chat Frame
    chat_frame = Frame(root1, width=380, height=551, bg=chatBgColor)
    chat_frame.pack(padx=10)
    chat_frame.pack_propagate(0)

    bottomFrame1 = Frame(root1, bg='#dfdfdf', height=100)
    bottomFrame1.pack(fill=X, side=BOTTOM)
    VoiceModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    VoiceModeFrame.pack(fill=BOTH)
    TextModeFrame = Frame(bottomFrame1, bg='#dfdfdf')
    TextModeFrame.pack(fill=BOTH)

    # VoiceModeFrame.pack_forget()
    TextModeFrame.pack_forget()

    cblLightImg = PhotoImage(file='extrafiles/images/centralButton.png')
    cblDarkImg = PhotoImage(file='extrafiles/images/centralButton1.png')
    if KCS_IMG == 1:
        cblimage = cblDarkImg
    else:
        cblimage = cblLightImg
    cbl = Label(VoiceModeFrame, fg='white', image=cblimage, bg='#dfdfdf')
    cbl.pack(pady=17)
    AITaskStatusLbl = Label(VoiceModeFrame, text='    Offline',
                            fg='white', bg=AITaskStatusLblBG, font=('montserrat', 16))
    AITaskStatusLbl.place(x=140, y=32)

    # Settings Button
    sphLight = PhotoImage(file="extrafiles/images/setting.png")
    sphLight = sphLight.subsample(2, 2)
    sphDark = PhotoImage(file="extrafiles/images/setting1.png")
    sphDark = sphDark.subsample(2, 2)
    if KCS_IMG == 1:
        sphimage = sphDark
    else:
        sphimage = sphLight
    settingBtn = Button(VoiceModeFrame, image=sphimage, height=30, width=30, bg='#dfdfdf',
                        borderwidth=0, activebackground="#dfdfdf", command=lambda: raise_frame(root2))
    settingBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Keyboard Button
    kbphLight = PhotoImage(file="extrafiles/images/keyboard.png")
    kbphLight = kbphLight.subsample(2, 2)
    kbphDark = PhotoImage(file="extrafiles/images/keyboard1.png")
    kbphDark = kbphDark.subsample(2, 2)
    if KCS_IMG == 1:
        kbphimage = kbphDark
    else:
        kbphimage = kbphLight
    kbBtn = Button(VoiceModeFrame, image=kbphimage, height=30, width=30, bg='#dfdfdf',
                   borderwidth=0, activebackground="#dfdfdf", command=changeChatMode)
    kbBtn.place(x=25, y=30)

    # Mic
    micImg = PhotoImage(file="extrafiles/images/mic.png")
    micImg = micImg.subsample(2, 2)
    micBtn = Button(TextModeFrame, image=micImg, height=30, width=30, bg='#dfdfdf',
                    borderwidth=0, activebackground="#dfdfdf", command=changeChatMode)
    micBtn.place(relx=1.0, y=30, x=-20, anchor="ne")

    # Text Field
    TextFieldImg = PhotoImage(file='extrafiles/images/textField.png')
    UserFieldLBL = Label(TextModeFrame, fg='white',
                         image=TextFieldImg, bg='#dfdfdf')
    UserFieldLBL.pack(pady=17, side=LEFT, padx=10)
    UserField = Entry(TextModeFrame, fg='white', bg='#203647', font=(
        'Montserrat', 16), bd=6, width=22, relief=FLAT)
    UserField.place(x=20, y=30)
    UserField.insert(0, "Ask me anything...")
    UserField.bind('<Return>', keyboardInput)

    # User and Bot Icon
    userIcon = PhotoImage(
        file="extrafiles/images/avatars/ChatIcons/a"+str(ownerPhoto)+".png")
    botIcon = PhotoImage(file="extrafiles/images/assistant2.png")
    botIcon = botIcon.subsample(2, 2)

    ###########################
    ########  SETTINGS  #######
    ###########################

    settingsLbl = Label(root2, text='Settings', font=(
        'Arial Bold', 15), bg=background, fg=textColor)
    settingsLbl.pack(pady=10)
    separator = ttk.Separator(root2, orient='horizontal')
    separator.pack(fill=X)
    # User Photo
    userProfileImg = Image.open(
        "extrafiles/images/avatars/a"+str(ownerPhoto)+".png")
    userProfileImg = ImageTk.PhotoImage(userProfileImg.resize((120, 120)))
    userPhoto = Button(root2, image=userProfileImg, bg=background, bd=0,
                       relief=FLAT, activebackground=background, command=SelectAvatar)
    userPhoto.pack(pady=(20, 5))

    # Change Photo
    chngPh = ImageTk.PhotoImage(Image.open(
        "extrafiles/images/avatars/changephoto2.png").resize((120, 120)))

    userPhoto.bind('<Enter>', onhover)
    userPhoto.bind('<Leave>', onleave)

    # Username
    userName = Label(root2, text=ownerName, font=(
        'Arial Bold', 15), fg=textColor, bg=background)
    userName.pack()

    # Settings Frame
    settingsFrame = Frame(root2, width=300, height=300, bg=background)
    settingsFrame.pack(pady=20)

    assLbl = Label(settingsFrame, text='Assistant Voice',
                   font=('Arial', 13), fg=textColor, bg=background)
    assLbl.place(x=0, y=20)
    n = StringVar()
    assVoiceOption = ttk.Combobox(settingsFrame, values=(
        'Female', 'Male'), font=('Arial', 13), width=13, textvariable=n)
    assVoiceOption.current(voice_id)
    assVoiceOption.place(x=150, y=20)
    assVoiceOption.bind('<<ComboboxSelected>>', changeVoice)

    voiceRateLbl = Label(settingsFrame, text='Voice Rate',
                         font=('Arial', 13), fg=textColor, bg=background)
    voiceRateLbl.place(x=0, y=60)
    n2 = StringVar()
    voiceOption = ttk.Combobox(settingsFrame, font=(
        'Arial', 13), width=13, textvariable=n2)
    voiceOption['values'] = ('Very Low', 'Low', 'Normal', 'Fast', 'Very Fast')
    voiceOption.current(ass_voiceRate//50-2)  # 100 150 200 250 300
    voiceOption.place(x=150, y=60)
    voiceOption.bind('<<ComboboxSelected>>', changeVoiceRate)

    volumeLbl = Label(settingsFrame, text='Volume', font=(
        'Arial', 13), fg=textColor, bg=background)
    volumeLbl.place(x=0, y=105)
    volumeBar = Scale(settingsFrame, bg=background, fg=textColor, sliderlength=30, length=135, width=16,
                      highlightbackground=background, orient='horizontal', from_=0, to=100, command=changeVolume)
    volumeBar.set(int(ass_volume*100))
    volumeBar.place(x=150, y=85)

    themeLbl = Label(settingsFrame, text='Theme', font=(
        'Arial', 13), fg=textColor, bg=background)
    themeLbl.place(x=0, y=143)
    themeValue = IntVar()
    s = ttk.Style()
    s.configure('Wild.TRadiobutton', font=('Arial Bold', 10), background=background,
                foreground=textColor, focuscolor=s.configure(".")["background"])
    darkBtn = ttk.Radiobutton(settingsFrame, text='Dark', value=1, variable=themeValue,
                              style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
    darkBtn.place(x=150, y=145)
    lightBtn = ttk.Radiobutton(settingsFrame, text='Light', value=2, variable=themeValue,
                               style='Wild.TRadiobutton', command=changeTheme, takefocus=False)
    lightBtn.place(x=230, y=145)
    themeValue.set(1)
    if KCS_IMG == 0:
        themeValue.set(2)

    chooseChatLbl = Label(settingsFrame, text='Chat Background', font=(
        'Arial', 13), fg=textColor, bg=background)
    chooseChatLbl.place(x=0, y=180)
    cimg = PhotoImage(file="extrafiles/images/colorchooser.png")
    cimg = cimg.subsample(3, 3)
    colorbar = Label(settingsFrame, bd=3, width=18, height=1, bg=chatBgColor)
    colorbar.place(x=150, y=180)
    if KCS_IMG == 0:
        colorbar['bg'] = '#E8EBEF'
    Button(settingsFrame, image=cimg, relief=FLAT,
           command=getChatColor).place(x=261, y=180)

    backBtn = Button(settingsFrame, text='   Back   ', bd=0, font=(
        'Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=lambda: raise_frame(root1))
    clearFaceBtn = Button(settingsFrame, text='   Clear Facial Data   ', bd=0, font=(
        'Arial 12'), fg='white', bg='#14A769', relief=FLAT, command=deleteUserData)
    backBtn.place(x=5, y=250)
    clearFaceBtn.place(x=120, y=250)

    try:
        # pass
        Thread(target=voiceMedium).start()
    except:
        pass
    try:
        # pass
        Thread(target=webScrapping.dataUpdate).start()
    except Exception as e:
        print('System is Offline...')

    root.iconbitmap('extrafiles/images/assistant2.ico')
    raise_frame(root1)
    root.mainloop()