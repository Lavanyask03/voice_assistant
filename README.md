# About
Voice Assistant in Python using speech recognition. The application takes in voice commands
from the user and performs the respective tasks like:
* Launch any system application
* Tell the time
* Play a song
* Send an email
* Tell the news or top stories
* Answer your questions by searching the web
* Open the search query in Google, Wikipedia and YouTube. 

# Run on local machine
1. Clone the repository
```
git clone https://github.com/Lavanyask03/voice_assistant.git
```

2. Install required packages using
  - Python 2: `pip install -r requirements.txt`
  - Python 3: `pip3 install -r requirements.txt`
      
3. Run the program
```
python voice_assistant.py
```

## Note:
Make sure to change the paths for:
  - applications in launch_app(app) function
  - chromedriver.exe in get_answers(query) and search_web(command) function
  
Do add your email credentials in the send_email() function and also turn on Less Secure Apps
