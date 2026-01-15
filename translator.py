"""
Real-Time Voice Translator - Desktop Application
Works with Zoom, Meet, WhatsApp, any application

Requirements:
pip install pyaudio speechrecognition pyttsx3 deep-translator
"""

import speech_recognition as sr
from deep_translator import GoogleTranslator
import threading
import queue
import time
import sys

class RealTimeTranslator:
    def __init__(self, source_lang='hi', target_lang='en'):
        """
        source_lang: 'hi' for Hindi, 'en' for English
        target_lang: 'en' for English, 'hi' for Hindi
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Set voice based on target language
        self._set_voice()
        
        # Initialize translator
        self.translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        # Queue for translations
        self.translation_queue = queue.Queue()
        
        # Control flags
        self.is_running = False
        self.is_speaking = False
        
        print(f"✅ Translator initialized: {source_lang} → {target_lang}")
    
    def _set_voice(self):
        """Set appropriate voice for target language"""
        try:
            voices = self.tts_engine.getProperty('voices')
            
            for voice in voices:
                if self.target_lang == 'hi' and 'hindi' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    return
                elif self.target_lang == 'en' and 'english' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    return
            
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"⚠️  Voice setting warning: {e}")
    
    def translate_text(self, text):
        """Translate text from source to target language"""
        try:
            translation = self.translator.translate(text)
            return translation
        except Exception as e:
            print(f"❌ Translation error: {e}")
            try:
                self.translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
                translation = self.translator.translate(text)
                return translation
            except:
                return None
    
    def speak(self, text):
        """Speak the translated text"""
        if text and not self.is_speaking:
            self.is_speaking = True
            print(f"🔊 Speaking: {text}")
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"❌ Speech error: {e}")
            finally:
                self.is_speaking = False
    
    def process_audio(self, audio_data):
        """Process audio and translate"""
        try:
            print("🎤 Recognizing speech...")
            
            speech_lang_map = {
                'hi': 'hi-IN',
                'en': 'en-US',
                'es': 'es-ES',
                'fr': 'fr-FR',
                'de': 'de-DE',
                'ja': 'ja-JP',
                'zh-CN': 'zh-CN',
                'ar': 'ar-SA'
            }
            
            speech_lang = speech_lang_map.get(self.source_lang, self.source_lang)
            
            text = self.recognizer.recognize_google(audio_data, language=speech_lang)
            print(f"📝 You said: {text}")
            
            translation = self.translate_text(text)
            if translation:
                print(f"🌐 Translation: {translation}")
                self.translation_queue.put(translation)
            
        except sr.UnknownValueError:
            print("❓ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ API error: {e}")
        except Exception as e:
            print(f"❌ Processing error: {e}")
    
    def speaker_thread(self):
        """Thread to speak translations"""
        while self.is_running:
            try:
                translation = self.translation_queue.get(timeout=1)
                self.speak(translation)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Speaker thread error: {e}")
    
    def listening_loop(self, source):
        """Main listening loop"""
        while self.is_running:
            try:
                print("\n👂 Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                # Process in separate thread
                threading.Thread(
                    target=self.process_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                if self.is_running:
                    print(f"⚠️  Listening error: {e}")
                    time.sleep(0.5)
    
    def start(self):
        """Start listening and translating"""
        print("\n" + "="*60)
        print("🚀 REAL-TIME TRANSLATOR STARTED")
        print("="*60)
        print(f"📌 Translating: {self.source_lang.upper()} → {self.target_lang.upper()}")
        print("🎤 Speak naturally into your microphone")
        print("⏹️  Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        self.is_running = True
        
        # Start speaker thread
        speaker = threading.Thread(target=self.speaker_thread, daemon=True)
        speaker.start()
        
        # Start listening
        try:
            mic = sr.Microphone()
            
            with mic as source:
                print("🎧 Adjusting for ambient noise... (wait 2 seconds)")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("✅ Ready! Start speaking...\n")
                
                try:
                    self.listening_loop(source)
                except KeyboardInterrupt:
                    print("\n\n⏹️  Stopping translator...")
                    self.is_running = False
                    print("✅ Translator stopped")
                    
        except OSError as e:
            print(f"\n❌ Microphone Error: {e}")
            print("\n💡 Solutions:")
            print("1. Check if microphone is connected")
            print("2. Grant microphone permission to Python")
            print("3. Close other apps using microphone (Discord, Zoom, etc.)")
            print("4. Try running as administrator")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    def swap_languages(self):
        """Swap source and target languages"""
        self.source_lang, self.target_lang = self.target_lang, self.source_lang
        self.translator = GoogleTranslator(source=self.source_lang, target=self.target_lang)
        self._set_voice()
        print(f"🔄 Languages swapped: {self.source_lang} → {self.target_lang}")


def list_microphones():
    """List all available microphones"""
    print("\n🎤 Available Microphones:")
    print("-" * 50)
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{index}: {name}")
    print("-" * 50)


def main():
    """Main function"""
    print("\n" + "="*60)
    print("        REAL-TIME VOICE TRANSLATOR")
    print("="*60)
    
    # Check microphone availability
    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            print("\n❌ No microphone detected!")
            print("Please connect a microphone and try again.")
            return
        print(f"\n✅ Found {len(mics)} microphone(s)")
    except Exception as e:
        print(f"\n❌ Error checking microphones: {e}")
        return
    
    print("\nSelect mode:")
    print("1. Hindi → English")
    print("2. English → Hindi")
    print("3. Spanish → English")
    print("4. English → Spanish")
    print("5. Custom languages")
    print("6. List available microphones")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == '6':
        list_microphones()
        return main()
    
    if choice == '1':
        translator = RealTimeTranslator(source_lang='hi', target_lang='en')
    elif choice == '2':
        translator = RealTimeTranslator(source_lang='en', target_lang='hi')
    elif choice == '3':
        translator = RealTimeTranslator(source_lang='es', target_lang='en')
    elif choice == '4':
        translator = RealTimeTranslator(source_lang='en', target_lang='es')
    elif choice == '5':
        print("\nSupported language codes:")
        print("hi=Hindi, en=English, es=Spanish, fr=French, de=German")
        print("ja=Japanese, zh-CN=Chinese, ar=Arabic, ru=Russian, pt=Portuguese")
        source = input("\nSource language code: ").strip().lower()
        target = input("Target language code: ").strip().lower()
        translator = RealTimeTranslator(source_lang=source, target_lang=target)
    else:
        print("Invalid choice. Using default: Hindi → English")
        translator = RealTimeTranslator(source_lang='hi', target_lang='en')
    
    # Start translator
    try:
        translator.start()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
