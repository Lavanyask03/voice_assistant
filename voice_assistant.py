# importing all the required packages
from gtts import gTTS
from playsound import playsound
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
import speech_recognition as sr
import requests
import smtplib
import os
import sys
import re
import random
import datetime

# set a running global variable to indicate when to terminate
#running = True

# the assistant speaks any text passed to it
def assistant_speaks(text):
    print(text)
    # call gTTS
    speech = gTTS(text=text,lang='en',slow=False)
    file = "speech.mp3"
    # save the audio file as speech.mp3
    speech.save(file) 
    playsound(file,True)
    # delete the file after playing
    os.remove(file)

# get the command said by user
def get_command():
    # initialize recognizer and microphone objects
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("Listening...")
    with mic as source:
        print("Say something!")
        # play a ping sound for start
        # playsound("..\\audio\\message_sound.wav")
        # reduce background noise
        r.adjust_for_ambient_noise(source,duration=0.5)
        # listen for time limit 10 secs
        audio = r.listen(source,timeout=10)
    print("Stop!!")
    command = ""
    try:
        command = r.recognize_google(audio)
        print("You said " + command + "\n")
    except:
        print("Could not understand you. Please try again.")
        command = get_command()
    return command.lower()

# process the command and respond to it
def process_command(command):
    try:
        # launch an application
        if "launch" in command:
            app = command.split(" ",1)[-1]
            launch_app(app)

        # tell the time
        elif "time" in command:
            now = datetime.datetime.now()
            assistant_speaks('Current time is %d hours %d minutes' % (now.hour, now.minute))
        
        # play a song
        elif "play me a song" in command:
            play_song()

        # send an email
        elif "email" in command:
            send_email()
        
        # search the web for results
        elif "search" in command:
            search_web(command)

        # tell the news / top stories
        elif "news" in command or "top stories" in command:
            news_today()

        # tell the user what tasks can he ask for
        elif "help me" in command:
            assistant_speaks("""
            You can use the following commands and I can help you out.
            1. Launch application: Launches any system application.
            2. Time: Tells the current time.
            3. Play me a song: Plays a random song from system library.
            4. Send an email: Sends an email from lavanya03sk@gmail.com.
            5. Search xyz: Searches xyz on the internet and gives results.
            6. Search in youtube, wikipedia or google: Opens the search queries in the respective websites.
            7. Ask anything: Get answers from the internet or get search results from google.
            8. Ask for news or topstories: Tells all the latest news.
            """)

        # terminate the program
        elif command.lower() in ["exit","goodbye","quit","shutdown"]:
            assistant_speaks("Bye Bye.")
            # set the running variable to False to exit the program
            global running
            running = False

        # default
        else:
            assistant_speaks("Searching the web for answers.")
            search_web(command)

    except:
        assistant_speaks("I could not understand you, I can search the web for you, Do you want to continue?")
        ans = get_command()
        if ans in ["yes","yeah","ok"]:
            search_web(command)

# launch system applications
def launch_app(app):
    assistant_speaks("Launching " + app)
    program = app.lower()
    if app.lower() == "calculator":
        program = "calc"
    elif app.lower() == "wordpad":
        program = "write"
    elif app.lower() == "command prompt":
        program = "cmd"
    elif app.lower() == "sublime text":
        program = app.replace(' ','_')
    elif app.lower() == "excel":
        program = "C:\\Program Files\\Microsoft Office\\Office16\\EXCEL" # paste path for EXCEL.exe on your computer
    elif app.lower() == "word":
        program = "C:\\Program Files\\Microsoft Office\\Office16\\WINWORD" # paste path for WINWORD.exe on your computer
    elif app.lower() == "powerpoint":
        program = "C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT" # paste path for POWERPNT.exe on your computer
    else:
        program = app.replace(' ','')
    try:
        os.startfile(program + ".exe") # run the desired application
    except FileNotFoundError:
        assistant_speaks("Could not open app")

# search answers from internet and respond
def get_answers(query):
    # use chrome driver to get the page
    # download chrome driver from https://chromedriver.chromium.org/downloads
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Add the path to chromedriver.exe file on your computer
    driver = webdriver.Chrome("C:/Users/Lavanya.DESKTOP-SIIUMJV/chromedriver_win32/chromedriver.exe",options=chrome_options)
    driver.wait = WebDriverWait(driver,5)
    query_string = query.replace(' ','+')
    # set the url
    url = "https://www.google.com/search?q=" + query_string
    driver.get(url)
    try:
        driver.wait.until(ec.presence_of_element_located((By.CLASS_NAME,"gsfi")))
    except:
        print("FAILED!!")
    soup = BeautifulSoup(driver.page_source,"html.parser")
    ans = soup.find_all(class_="Z0LcW XcVN5d") # if answer is a single word
    if ans:
        answer = ans[0].get_text()
    if not ans: # if answer is a set of steps
        ans = [x.text for x in soup.find('ol', {'class': 'X5LH0c'}).find_all('li')] 
        answer = ", ".join(ans)
    if not ans: # if no specific answer is found return 0
        answer = 0
    return answer

# play a song from sytem library
def play_song():
    # set path to folder where music files are present on your computer
    path = "C:\\Users\\Lavanya.DESKTOP-SIIUMJV\\Music"
    files = os.listdir(path)
    # choose a random music/song file to play from the given folder
    d = random.choice(files)
    assistant_speaks("Playing song")
    os.startfile(path + "\\" + d)

# get latest news and top stories
def news_today():
    r = requests.get("https://news.google.com/topstories")
    soup = BeautifulSoup(r.content,"html.parser")
    news_list = soup.find_all("h3",{"class":"ipQwMb ekueJc gEATFF RD0gLb"})
    news = []
    # get the top 20 elements in the topstories
    for n in news_list[:20]:
        news.append(n.get_text())
    assistant_speaks(",".join(news))

# open search results on the web - Google, YouTube, Wikipedia
def search_web(command):
    # change the executable path to the path of chromedriver.exe on your computer
    driver = webdriver.Chrome(executable_path="C:/Users/Lavanya.DESKTOP-SIIUMJV/chromedriver_win32/chromedriver.exe")
    driver.implicitly_wait(1)
    driver.maximize_window()

    # YouTube
    if "youtube" in command:
        assistant_speaks("Opening in youtube")
        indx = command.lower().split().index('youtube') # get starting index of the search query
        query = command.split()[indx + 1:] # get the search query as list
        driver.get("https://www.youtube.com/results?search_query=" + '+'.join(query))
        return

    # Wikipedia
    elif "wikipedia" in command:
        assistant_speaks("Opening in wikipedia")
        indx = command.lower().split().index('wikipedia') # get starting index of the search query
        query = command.split()[indx + 1:] # get the search query as list
        driver.get("https://en.wikipedia.org/wiki/" + '_'.join(query))
        return

    #google
    elif "google" in command:
        assistant_speaks("Opening in google")
        indx = command.lower().split().index('google') # get starting index of the search query
        query = command.split()[indx + 1:] # get the search query as list
        driver.get("https://www.google.com/search?q=" + '+'.join(query))
        return

    elif "search" in command:
        assistant_speaks("Searching in google")
        indx = command.lower().split().index('search') # get starting index of the search query
        query = command.split()[indx + 1:] # get the search query as list
        driver.get("https://www.google.com/search?q=" + '+'.join(query))
        return

    else:
        answer = get_answers(command)
        if answer: # if any answer is returned
            assistant_speaks(answer)
        else: # if answer = 0
            assistant_speaks("Here are some results I found on the internet.")
            driver.get("https://www.google.com/search?q=" + '+'.join(command))
        return

# send an email
def send_email():
    # get the recipient
    assistant_speaks("Who is the recipient")
    to_address = get_command() + '@gmail.com'
    if not to_address: # if 0 is returned set to_address to default
        to_address = 'YOUR_DEFAULT_EMAILID' # set a default email address
    # use smtplib to connect to gmail
    conn = smtplib.SMTP('smtp.gmail.com',587) # Port number can be 465 or 587
    conn.ehlo()
    # ensure transport layer security
    conn.starttls()
    username = '' # Add your emailid from which email is to be sent
    password = '' # Add your password
    # Make sure that you turn on Less Secure Apps on the gmail settings
    # Go to > Manage your Google Account > Security > Less secure app access > ON
    conn.login(username,password)
    assistant_speaks("What is the message")
    message = get_command()
    if message:
        content = 'Subject: TEST\n\n' + message + '.\n\n'
        conn.sendmail(username,to_address,content)
        conn.quit()
        assistant_speaks("Email sent successfully")
    else:
        assistant_speaks("I don't know what you mean")

# Driver code to run until user wants to exit
running = True
assistant_speaks("Hi User, I am Python Voice Assistant and I am your personal voice assistant, Please give a command or say 'help me' and I will tell you what all I can do for you.")
# loop to continue executing multiple commands
while running:
    process_command(get_command())