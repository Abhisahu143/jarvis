"""
JARVIS - Just A Rather Very Intelligent System
A professional voice assistant with advanced features and natural language processing.
"""

import sys
import os
import json
import time
import datetime
import logging
import random
import webbrowser
import requests
import wikipedia
import pyautogui
import psutil
import speedtest
import wolframalpha
from pathlib import Path
from typing import Optional, Dict, Any
from gtts import gTTS
import pygame
import speech_recognition as sr
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jarvis.log'),
        logging.StreamHandler()
    ]
)

# Initialize pygame mixer
pygame.mixer.init()

class Jarvis:
    def __init__(self):
        """Initialize Jarvis with configuration and settings"""
        self.name = "Jarvis"
        self.user = "Sir"
        self.recognizer = sr.Recognizer()
        self.load_config()
        self.setup_apis()
        self.commands = self.load_commands()
        
    def load_config(self):
        """Load configuration from config.json"""
        try:
            with open('config.json', 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "user": {
                    "name": "Sir",
                    "email": "",
                    "password": ""
                },
                "paths": {
                    "music": "",
                    "documents": "",
                    "downloads": ""
                },
                "apis": {
                    "wolframalpha": "",
                    "openweathermap": "",
                    "newsapi": ""
                },
                "preferences": {
                    "voice_speed": 1.0,
                    "language": "en",
                    "temperature_unit": "celsius"
                }
            }
            self.save_config()
            print("Created default config.json. Please update it with your settings.")
    
    def save_config(self):
        """Save configuration to config.json"""
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def setup_apis(self):
        """Initialize API clients"""
        try:
            self.wolfram_client = wolframalpha.Client(self.config['apis']['wolframalpha'])
        except:
            self.wolfram_client = None
            logging.warning("WolframAlpha API not configured")

    def load_commands(self) -> Dict[str, Any]:
        """Load command definitions"""
        return {
            'greeting': ['hello', 'hi', 'hey', 'greetings'],
            'farewell': ['bye', 'goodbye', 'see you', 'exit', 'quit'],
            'time': ['time', 'what time', 'current time'],
            'date': ['date', 'what date', 'current date', 'day'],
            'weather': ['weather', 'temperature', 'forecast'],
            'search': ['search', 'look up', 'find', 'google'],
            'wikipedia': ['wikipedia', 'wiki', 'who is', 'what is'],
            'system': ['cpu', 'memory', 'battery', 'system'],
            'music': ['play music', 'play song', 'music'],
            'volume': ['volume up', 'volume down', 'mute'],
            'screenshot': ['screenshot', 'capture screen'],
            'reminder': ['remind me', 'set reminder', 'reminder'],
            'joke': ['tell joke', 'joke', 'make me laugh'],
            'news': ['news', 'headlines', 'latest news'],
            'email': ['email', 'send email', 'check email'],
            'calculator': ['calculate', 'math', 'solve'],
            'translate': ['translate', 'translation'],
            'speedtest': ['speed test', 'internet speed', 'connection speed']
        }

    def speak(self, text: str) -> None:
        """Convert text to speech using gTTS and play with pygame"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_filename = temp_file.name
            
            tts = gTTS(text=text, lang=self.config['preferences']['language'])
            tts.save(temp_filename)
            
            # Play audio using pygame
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            # Clean up
            pygame.mixer.music.unload()
            os.unlink(temp_filename)
            
        except Exception as e:
            logging.error(f"Error in speech synthesis: {e}")
            print(f"Error in speech synthesis: {e}")

    def listen(self) -> Optional[str]:
        """Listen for user input and convert to text"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language=self.config['preferences']['language'])
            print(f"User said: {query}")
            return query.lower()
            
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except Exception as e:
            logging.error(f"Error in speech recognition: {e}")
            return None

    def get_time(self) -> str:
        """Get current time in a natural format"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}"

    def get_date(self) -> str:
        """Get current date in a natural format"""
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {current_date}"

    def get_weather(self, city: str) -> str:
        """Get weather information for a city"""
        try:
            api_key = self.config['apis']['openweathermap']
            if not api_key:
                return "Weather API not configured. Please update config.json"
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if data["cod"] == 200:
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"]
                humidity = data["main"]["humidity"]
                wind = data["wind"]["speed"]
                
                return f"The temperature in {city} is {temp}°C with {desc}. Humidity is {humidity}% and wind speed is {wind} m/s"
            return "Sorry, I couldn't get the weather information."
        except Exception as e:
            logging.error(f"Error getting weather: {e}")
            return "Sorry, I couldn't get the weather information."

    def get_system_info(self) -> str:
        """Get system information"""
        try:
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            battery = psutil.sensors_battery()
            
            info = f"CPU usage is {cpu_percent}%. "
            info += f"Memory usage is {memory.percent}%. "
            
            if battery:
                info += f"Battery is at {battery.percent}%"
                if battery.power_plugged:
                    info += " and charging"
            else:
                info += "Battery information not available"
                
            return info
        except Exception as e:
            logging.error(f"Error getting system info: {e}")
            return "Sorry, I couldn't get the system information"

    def get_news(self) -> str:
        """Get latest news headlines"""
        try:
            api_key = self.config['apis']['newsapi']
            if not api_key:
                return "News API not configured. Please update config.json"
                
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
            response = requests.get(url)
            news = response.json()
            
            if news["status"] == "ok":
                headlines = [article["title"] for article in news["articles"][:5]]
                return "Here are the top headlines: " + ". ".join(headlines)
            return "Sorry, I couldn't get the news"
        except Exception as e:
            logging.error(f"Error getting news: {e}")
            return "Sorry, I couldn't get the news"

    def calculate(self, query: str) -> str:
        """Calculate mathematical expressions"""
        try:
            if self.wolfram_client:
                res = self.wolfram_client.query(query)
                return next(res.results).text
            return "Calculator API not configured"
        except Exception as e:
            logging.error(f"Error in calculation: {e}")
            return "Sorry, I couldn't perform that calculation"

    def take_screenshot(self) -> str:
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            return f"Screenshot saved as {filename}"
        except Exception as e:
            logging.error(f"Error taking screenshot: {e}")
            return "Sorry, I couldn't take a screenshot"

    def check_internet_speed(self) -> str:
        """Check internet connection speed"""
        try:
            st = speedtest.Speedtest()
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000
            return f"Download speed is {download:.2f} Mbps and upload speed is {upload:.2f} Mbps"
        except Exception as e:
            logging.error(f"Error checking internet speed: {e}")
            return "Sorry, I couldn't check the internet speed"

    def process_command(self, query: str) -> None:
        """Process user commands"""
        if not query:
            return

        # Check for greetings
        if any(word in query for word in self.commands['greeting']):
            self.speak(f"Hello {self.user}, how can I help you?")
            return

        # Check for farewell
        if any(word in query for word in self.commands['farewell']):
            self.speak(f"Goodbye {self.user}, have a great day!")
            sys.exit(0)

        # Time related
        if any(word in query for word in self.commands['time']):
            self.speak(self.get_time())
            return

        # Date related
        if any(word in query for word in self.commands['date']):
            self.speak(self.get_date())
            return

        # Weather related
        if any(word in query for word in self.commands['weather']):
            city = query.replace("weather in", "").replace("weather", "").strip()
            if city:
                self.speak(self.get_weather(city))
            else:
                self.speak("Please specify a city")
            return

        # System information
        if any(word in query for word in self.commands['system']):
            self.speak(self.get_system_info())
            return

        # News
        if any(word in query for word in self.commands['news']):
            self.speak(self.get_news())
            return

        # Calculator
        if any(word in query for word in self.commands['calculator']):
            self.speak(self.calculate(query))
            return

        # Screenshot
        if any(word in query for word in self.commands['screenshot']):
            self.speak(self.take_screenshot())
            return

        # Internet speed
        if any(word in query for word in self.commands['speedtest']):
            self.speak(self.check_internet_speed())
            return

        # Wikipedia search
        if any(word in query for word in self.commands['wikipedia']):
            try:
                query = query.replace("wikipedia", "").replace("wiki", "").strip()
                self.speak(f"Searching Wikipedia for {query}")
                results = wikipedia.summary(query, sentences=2)
                self.speak("According to Wikipedia")
                print(results)
                self.speak(results)
            except Exception as e:
                logging.error(f"Error searching Wikipedia: {e}")
                self.speak("Sorry, I couldn't find that information")
            return

        # Web search
        if any(word in query for word in self.commands['search']):
            query = query.replace("search", "").replace("look up", "").strip()
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            self.speak(f"Searching for {query}")
            return

        # If no command matches
        self.speak("I'm not sure how to help with that. Could you please rephrase?")

def main():
    print("Initializing JARVIS...")
    print("\nAvailable Commands:")
    print("- Greetings (hello, hi, hey)")
    print("- Time and date")
    print("- Weather information")
    print("- System information")
    print("- News headlines")
    print("- Web searches")
    print("- Wikipedia lookups")
    print("- Calculations")
    print("- Screenshots")
    print("- Internet speed test")
    print("- Exit (bye, goodbye)")
    print("\nStarting JARVIS...")
    
    try:
        jarvis = Jarvis()
        jarvis.speak(f"Hello {jarvis.user}, I am {jarvis.name}, your personal assistant. How may I help you?")
        
        while True:
            query = jarvis.listen()
            if query:
                jarvis.process_command(query)
    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        logging.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 