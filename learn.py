import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import subprocess
import platform
import pygetwindow as gw
import pyautogui
import time
from threading import Timer
import shutil
from twilio.rest import Client
import openai

engine = pyttsx3.init('sapi5')

list = []
voices = engine.getProperty('voices')
# print(voices[0].id)

     
engine.setProperty('voice',voices[1].id)

def speak(audio):
 try:
  engine.say(audio)
  engine.runAndWait()
 except Exception as e :
     speak(e)
     print(e)

def wishMe(): 
 hour = int(datetime.datetime.now().hour)
 if 0 <= hour < 12:
    speak("Good morning")
 elif 12 <= hour < 18:
    speak("Good afternoon")
 elif 18 <= hour <= 22:
    speak("Good evening")
 else:
    speak("Good night")
    
 speak("I am Jarvis sir. Please tell me how may i help you")

def takeCommand():
    
  r= sr.Recognizer()
  with sr.Microphone() as source:
      print("Listening....")
      r.pause_threshold  = 1
      audio = r.listen(source)
      
      try:
          print("Recognizing...")
          query = r.recognize_google(audio,language ='en-in')
          print(f"User said:{query}\n")   
          
      except Exception as e:
        #   print(e)
          print("Say that again please...")  
          return "None" 
      return query
  
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('gourangjain782@gmail.com', 'Gourang@123')
    server.sendmail('manishsethi1209@gmail.com', to, content)
    server.close()
    
def open_bluetooth():
    system_platform = platform.system().lower()

    if system_platform == "windows":
        try:
            # Run the command to enable Bluetooth on Windows
            subprocess.run(['powershell', '-Command', 'Start-Process "bthprops.cpl"'])
            speak('Bluetooth opened')
        except Exception as e:
            speak('error opening bluetooth')
 
def close_bluetooth():
    system_platform = platform.system().lower()

    if system_platform == "windows":
        try:
            # Run the command to enable Bluetooth on Windows
            command = 'Stop-Service -Name bthserv -Force'

# Run the PowerShell command
            subprocess.run(['powershell', '-Command', command])
            speak('Bluetooth closed')
        except Exception as e:
            speak('error closing bluetooth')

def enable_hotspot():
    system_platform = platform.system().lower()

    if system_platform == "windows":
        try:
            # Run the command to open Mobile Hotspot settings using PowerShell
            subprocess.run(['powershell', '-Command', 'Start-Process "ms-settings:network-mobilehotspot"'])
            print("Mobile Hotspot settings opened.")
        except Exception as e:
            print(f"Error opening Mobile Hotspot settings: {e}")
            
            
def close_youtube_page():
    try:
        # Get all open windows
        windows = gw.getWindowsWithTitle("YouTube")

        # Focus on the YouTube window and close the tab using keyboard shortcuts
        for window in windows:
            window.activate()
            time.sleep(1)
            pyautogui.hotkey("Ctrl", "w")
            speak("Closed YouTube page.")
    except Exception as e:
        speak(f"Error closing YouTube page: {e}")   
        
# def close_music():
#     try: 
#             os.rmdir('D:\\songs')    
#             speak(" music closed")
#     except Exception as e:
#         speak(f"Error closing music: {e}")  
      
def alarm(data):
    # Function to execute when the alarm goes off
    speak(f"{data}")
    # Add any additional functionality you want to occur when the alarm goes off here
    
def timeset(data, time_seconds):
    # Function to set the time for the alarm
     speak(f"Setting alarm for {time_seconds} seconds")
     timer = Timer(time_seconds, alarm, [data])
     timer.start()
            
        
def close_google_page():
    try:
        # Get all open windows
        windows = gw.getWindowsWithTitle("Google")

        # Focus on the YouTube window and close the tab using keyboard shortcuts
        for window in windows:
            window.activate()
            time.sleep(1)
            pyautogui.hotkey("Ctrl", "w")
            speak("Closed Google page.")
    except Exception as e:
        speak(f"Error closing YouTube page: {e}")    
        
# Twilio credentials
account_sid = 'AC8819dc4d9b19f58d3f9e9297333e5413'
auth_token = '630bec3262707f6d0b7233851c50a8ca'
twilio_number = '+15616009249'

# Create a Twilio client
client = Client(account_sid, auth_token)

def send_sms(to_number, mess):
    try:
        message = client.messages.create(
            body=mess,
            from_=twilio_number,
            to=to_number
        )
        print(f"Message sent with SID: {message.sid}")
        speak("message sent")
    except Exception as e:
        speak(e)
        print(f"Failed to send message: {e}")
        
# whatsapp message 
def send_sms(whatsnum, whatsmsg):
    try:
        whatsmessage = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f'{whatsmsg}',
        to=f'{whatsnum}'
)
        print(f"Message sent with SID: {whatsmessage.sid}")
        speak("message sent")
    except Exception as e:
        speak(e)
        print(f"Failed to send message: {e}")
        
        openai.api_key = "sk-proj-7QhBHClurlFdHvMuv19HT3BlbkFJSqNvAtkq5x4WGzvF52q4"
            
def get_response(prompt):
    try :
        response = openai.Complete.create(
            engine="text-davinci-003",
            prompt = prompt,
            max_tokens = 150
        )
        speak(response.choices[0].text.strip())
    except Exception as e:
        speak("Error getting data from gpt")

           
if __name__ == "__main__":
    wishMe()
    i=1 
    do = 0   
    while (i==1):
        if do == 1 :
          query = list[-1]
          do = 0
        
        else:
         query = takeCommand().lower()
         list.append(query)
        
    
    
        if 'wikipedia' in query:
            speak('searching wikipedia')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)
     
        elif 'open youtube'in query:
            webbrowser.open("youtube.com")
        elif 'open google'in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow'in query:
            webbrowser.open("stackoverflow.com")
        elif 'play music' in query:
            try:
                music_dir = 'D:\\songs'  #use unicode
                songs = os.listdir(music_dir)
                print(songs)
                os.startfile(os.path.join(music_dir,songs[0]))
            except Exception as e:
                print(e)
                speak("sorry i cannot play the music as your directory is empty")    
        elif 'the time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S") 
            speak("sir, the time is {strtime}")    
        elif 'code' in query:
            codePath = 'C:\\Users\\goura\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codePath)
        elif 'email to me' in query:
            try:
                speak('what should I say')
                content = takeCommand()
                to = "gourangjain782@gmail.com"
                sendEmail(to, content)
                speak("Email has been sent")
            except Exception as e:
             print(e)
             speak("sorry i am not able to sent this email")
             
        elif 'jarvis mute yourself' in query:
            speak("ok sir , i am muting myself")
            i=2     
        elif 'open bluetooth' in query:
            open_bluetooth()    
            
        elif 'open hotspot' in query:
            enable_hotspot()  
            speak('hotspot opened') 
        elif 'close hotspot' in query:
            enable_hotspot()   
            speak('hotspot closed')
        elif 'close youtube' in query:
            close_youtube_page()    
        elif 'close google' in query:
            close_google_page()    
        elif 'speak' in query:
            talk = query.replace("speak","")
            speak(talk);    
        elif 'set alarm' in query:
            speak("what to say")
            data = takeCommand()
            speak("For what time")
            time = takeCommand()
            time = time.replace("seconds" , "")
            print(time)
            try:
             timeset(data,float(time))
             print("Alarm is completed")
            except Exception as e :
             print(e)
        elif 'close music' in query:
            try: 
             os.close('"D:\\songs\\Ed Sheeran - Perfect.mp3"')   
             speak(" music closed")
            except Exception as e:
             speak(f"Error closing music: {e}") 
             print(e) 
        elif 'open' in query or 'website' in query:
            try :
                query = query.replace("open ","")
                query = query.replace(" website","") 
                query = query.replace(" ","")
                print(query)
                URL = f"https://{query}.com"
                webbrowser.open(URL)
                speak(f"{query} opended")
            except Exception as e :
                 speak(e)
                 print(e)      
        elif 'perform last action again' in query:
            try:
                do = 1 
            except Exception  as e :
                speak("cannot perform the last action")
                print(e)
        elif 'make message' in query :
            speak('To which number sms is to be sent')
            number = takeCommand()
            number = number.replace(" ","")
            speak('what sms is to be send')
            mess = takeCommand()
            print(f'+91{number}', f'{mess}')
            send_sms(f'+91{number}', f'{mess}')
        elif 'make whatsapp message' in query :
             speak('To which number whatsapp is to be sent')
             whatsappnum = takeCommand()
             whatsappnum = whatsappnum.replace(" ","")
             speak('what sms is to be send')
             whatsapp = takeCommand()        # it is the message that is to be sent
             print(f'+91{whatsappnum}', f'{whatsapp}')
             send_sms(f'whatsapp:+91{whatsappnum}', f'{whatsapp}')
        elif 'gpt' in query :
              speak("what is the prompt")
              prompt = takeCommand()
              get_response(prompt)
                
        print(list)
           




        


    


