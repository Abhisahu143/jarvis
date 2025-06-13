# JARVIS - Just A Rather Very Intelligent System

A professional voice assistant with advanced features and natural language processing capabilities, built in Python.

## Features

- Voice recognition and speech synthesis
- Natural language command processing
- Real-time system information monitoring
- Weather information retrieval
- News headlines
- Wikipedia searches
- Web searches
- Mathematical calculations using WolframAlpha
- Screenshot functionality
- Internet speed testing
- Time and date information

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Abhisahu143/jarvis.git
cd jarvis
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the `config.json` file with your API keys and preferences:
- WolframAlpha API
- OpenWeatherMap API
- NewsAPI

## Usage

Run JARVIS using:
```bash
python jarvis.py
```

### Available Commands

- Greetings: "hello", "hi", "hey"
- Time: "what time is it", "current time"
- Date: "what date is it", "current date"
- Weather: "weather in [city]"
- System Info: "system status", "cpu usage"
- News: "latest news", "headlines"
- Web Search: "search [query]"
- Wikipedia: "wiki [query]"
- Calculations: "calculate [expression]"
- Screenshot: "take screenshot"
- Internet Speed: "check internet speed"
- Exit: "goodbye", "bye"

## Requirements

- Python 3.7+
- See `requirements.txt` for complete list of dependencies

## Configuration

Update `config.json` with your personal settings:
```json
{
    "user": {
        "name": "Your Name",
        "email": "your.email@example.com"
    },
    "apis": {
        "wolframalpha": "YOUR_API_KEY",
        "openweathermap": "YOUR_API_KEY",
        "newsapi": "YOUR_API_KEY"
    }
}
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please open an issue in the repository's issue tracker.