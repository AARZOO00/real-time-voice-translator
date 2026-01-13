# server.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from deep_translator import GoogleTranslator
import speech_recognition as sr
import tempfile
from gtts import gTTS

app = FastAPI()

@app.post("/translate_audio/")
async def translate_audio(file: UploadFile = File(...), src_lang="auto", tgt_lang="en"):
    # save file
    tmp_in = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp_in.write(await file.read())
    tmp_in.flush()

    # ASR
    r = sr.Recognizer()
    with sr.AudioFile(tmp_in.name) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language=src_lang)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

    # translate
    translated = GoogleTranslator(source='auto', target=tgt_lang).translate(text)

    # tts
    tts = gTTS(translated, lang=tgt_lang[:2])
    tmp_out = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(tmp_out.name)

    return {"text": text, "translated": translated, "audio_url": tmp_out.name}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
