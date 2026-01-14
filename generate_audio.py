import pyttsx3

engine = pyttsx3.init()
engine.save_to_file("Hello, this is a test.", "test.wav")
engine.runAndWait()
