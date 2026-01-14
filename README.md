# 🌍 Universal Translator

A real-time voice translation application that works seamlessly with any desktop application including Zoom, Google Meet, WhatsApp, and more. Powered by advanced speech recognition and translation APIs.

## ✨ Features

- **Real-Time Voice Translation**: Speak naturally and get instant translations
- **Multiple Language Support**: Hindi ↔ English, Spanish ↔ English, and more
- **Desktop Integration**: Works with Zoom, Google Meet, WhatsApp, Teams, and any audio application
- **High Accuracy**: Uses Google Translate API and SpeechRecognition for reliable translations
- **Text-to-Speech**: Automatic audio output of translated text
- **Microphone Selection**: Choose from multiple microphones connected to your system
- **Adaptive Noise Cancellation**: Automatically adjusts to ambient noise levels
- **Two Interface Options**:
  - **Desktop Application** (`translator.py`): Interactive command-line interface
  - **REST API** (`backend/server.py`): FastAPI server for programmatic access

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A microphone
- Internet connection (for translation services)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd UniversalTranslator
   ```

2. **Install dependencies**
   ```bash
   pip install pyaudio speechrecognition pyttsx3 deep-translator anthropic fastapi uvicorn gtts
   ```

### Usage

#### Desktop Application

Run the interactive translator:

```bash
python translator.py
```

Then select your preferred translation mode:
1. Hindi → English
2. English → Hindi
3. Spanish → English
4. English → Spanish
5. Custom languages
6. List available microphones

#### REST API Server

Start the FastAPI server:

```bash
python backend/server.py
```

The API will be available at `http://localhost:8000`

**Endpoint**: `POST /translate_audio/`
- **Parameters**:
  - `file`: Audio file (WAV format)
  - `src_lang`: Source language code (default: "auto")
  - `tgt_lang`: Target language code (default: "en")

**Response**:
```json
{
  "text": "recognized text",
  "translated": "translated text",
  "audio_url": "path/to/output.mp3"
}
```

## 🏗️ Project Structure

```
UniversalTranslator/
├── translator.py          # Main desktop application
├── backend/
│   └── server.py         # FastAPI backend server
├── SETUP_GUIDE.md        # Detailed setup instructions
└── README.md             # This file
```

## 🔧 Configuration

### Source Language Codes
- `hi` - Hindi
- `en` - English
- `es` - Spanish
- `fr` - French
- `de` - German

### Speech Recognition Settings (in `translator.py`)

You can customize these parameters:
- `energy_threshold`: Adjust microphone sensitivity (default: 300)
- `pause_threshold`: Time to wait before ending speech capture (default: 0.8s)
- `rate`: Speech output speed (default: 150 words per minute)
- `volume`: Speaker volume (default: 0.9)

## 📋 Supported Languages

The translator supports all languages that Google Translate supports, including:
- Hindi, English, Spanish, French, German, Portuguese, Russian, Japanese, Mandarin, Arabic, and many more

## ⚠️ Troubleshooting

### "No module named" error
Make sure all dependencies are installed:
```bash
pip install --upgrade pyaudio speechrecognition pyttsx3 deep-translator
```

### Microphone not working
1. Run option 6 to list available microphones
2. Check Windows Audio settings
3. Ensure microphone is properly connected and enabled

### Poor speech recognition
- Speak clearly and at a moderate pace
- Reduce background noise
- Adjust `energy_threshold` value in the code (increase for noisy environments)

### Translation API issues
- Check your internet connection
- Try the "Custom languages" option to verify the service

## 📚 Dependencies

- **pyaudio**: Audio input capture
- **SpeechRecognition**: Speech-to-text conversion
- **pyttsx3**: Text-to-speech output
- **deep-translator**: Translation API wrapper
- **fastapi**: Web API framework (backend)
- **uvicorn**: ASGI server (backend)
- **gTTS**: Google Text-to-Speech service
- **anthropic**: Claude API integration (optional)

## 🎯 Use Cases

- **Language Learning**: Practice pronunciation with real-time feedback
- **Conference Calls**: Real-time translation during Zoom/Meet calls
- **Customer Support**: Communicate with international clients
- **Travel**: Break language barriers on the go
- **Content Creation**: Translate videos and audio content

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 📧 Support

For issues, questions, or suggestions, please create an issue in the repository.

---

**Made with ❤️ for global communication**
