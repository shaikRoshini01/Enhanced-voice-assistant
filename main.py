import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import requests
import os
import pyjokes
from config import WEATHER_API_KEY,NEWS_API_KEY

# Initialize engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)

def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        listener.adjust_for_ambient_noise(source)
        voice = listener.listen(source)
    try:
        command = listener.recognize_google(voice)
        command = command.lower()
        print(f"User said: {command}")
    except:
        command = ""
    return command
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        talk(f"The temperature in {city} is {temp} degrees Celsius with {desc}.")
    else:
        talk("City not found.")
def get_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?language=en&apiKey={NEWS_API_KEY}"
        response = requests.get(url)
        data = response.json()
        print(data)

        if data["status"] == "ok":
            articles = data["articles"][:5]
            news_list = []

            for article in articles:
                title = article["title"]
                news_list.append(title)

            talk("Here are the top news headlines.")
            for i, headline in enumerate(news_list, start=1):
                talk(f"Headline {i}. {headline}")

        else:
            talk("Sorry, I couldn't fetch news at the moment.")

    except Exception as e:
        talk("There was an error fetching the news.")
        print(e)
def calculate(command):
    try:
        expression = command.replace("calculate", "")
        result = eval(expression)
        talk(f"The answer is {result}")
    except:
        talk("Sorry, I couldn't calculate that.")

def greet_user():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        talk("Good morning Ammu!")
    elif 12 <= hour < 18:
        talk("Good afternoon Ammu!")
    else:
        talk("Good evening Ammu!")
    talk("How can I help you today?")

def remember_note():
    talk("What should I remember?")
    data = take_command()
    with open("notes.txt", "a") as f:
        f.write(data + "\n")
    talk("I will remember that.")

def recall_note():
    if os.path.exists("notes.txt"):
        with open("notes.txt", "r") as f:
            notes = f.read()
        talk(f"You asked me to remember these notes: {notes}")
    else:
        talk("You don't have any saved notes.")

def tell_joke():
    joke = pyjokes.get_joke()
    talk(joke)

def system_control(command):
    if "shutdown" in command:
        talk("Shutting down your system.")
        os.system("shutdown /s /t 5")
    elif "restart" in command:
        talk("Restarting your system.")
        os.system("shutdown /r /t 5")
    elif "open notepad" in command:
        os.system("notepad")
    elif "open calculator" in command:
        os.system("calc")

def run_alexa():
    greet_user()
    while True:
        command = take_command()

        if "time" in command:
            time = datetime.datetime.now().strftime("%H:%M")
            talk(f"The current time is {time}")

        elif "date" in command:
            date = datetime.datetime.now().strftime("%d %B %Y")
            talk(f"Today's date is {date}")
        elif "news" in command:
            talk("Fetching the latest news headlines.")
            get_news()
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "")
            info = wikipedia.summary(topic, sentences=2)
            talk(info)

        elif "play" in command:
            song = command.replace("play", "")
            talk(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif "weather" in command:
            talk("Which city?")
            city = take_command()
            get_weather(city)

        elif "calculate" in command:
            calculate(command)

        elif "joke" in command:
            tell_joke()

        elif "remember" in command:
            remember_note()

        elif "recall" in command or "note" in command:
            recall_note()

        elif "shutdown" in command or "restart" in command or "notepad" in command or "calculator" in command:
            system_control(command)

        elif "open google" in command:
            webbrowser.open("https://www.google.com")

        elif "open youtube" in command:
            webbrowser.open("https://www.youtube.com")

        elif "send message" in command:
            talk("To which number?")
            number = input("Enter WhatsApp number (with country code): ")
            talk("What message should I send?")
            message = take_command()
            pywhatkit.sendwhatmsg_instantly(number, message)
            talk("Message sent successfully!")

        elif "stop" in command or "exit" in command or "bye" in command:
            talk("Okay Roshini, shutting down. Have a great day!")
            break

        else:
            talk("Sorry, I didn't catch that. Please say again.")

if __name__ == "__main__":
    run_alexa()