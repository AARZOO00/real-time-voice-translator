from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from deep_translator import GoogleTranslator
import speech_recognition as sr
import tempfile
from gtts import gTTS

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/translate_audio/")
async def translate_audio(file: UploadFile = File(...), src_lang="auto", tgt_lang="en"):
    tmp_in = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_in.write(await file.read())
    tmp_in.flush()

    r = sr.Recognizer()
    with sr.AudioFile(tmp_in.name) as source:
        audio = r.record(source)

    try:
        text = r.recognize_google(audio)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    translated = GoogleTranslator(source='auto', target=tgt_lang).translate(text)

    tts = gTTS(translated, lang=tgt_lang[:2])
    tmp_out = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(tmp_out.name)

    return {
        "original": text,
        "translated": translated,
        "audio_file": tmp_out.name
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
