import logging
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
from gtts_lang_codes import check_for_translation_change


# Global settings
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename="logs.log", encoding="utf-8", level=logging.DEBUG)

recognizer = sr.Recognizer()
translator = Translator()
recognizer.dynamic_energy_threshold = False # stop mic from recording ambient noise
TRANSLATE_TO = "es"
ACTIVE_MODE = True



from ctypes import *
from contextlib import contextmanager
import pyaudio

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)








while True:
    logging.debug("-------------------------------------------")
    try: # The main loop always continues!
        with noalsaerr() as _, sr.Microphone() as source:
            text = None

            try:
                # Get Audio clip
                logging.debug("> Getting audio")
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                # Speech-to-text
                logging.debug("> Speech to text")
                try:
                    text = recognizer.recognize_google(audio, language="en-us")
                except sr.exceptions.UnknownValueError as e:
                    logging.warning("ERROR recognizing speech. See below:")
                    logging.warning(e)
                    pass

            except sr.exceptions.WaitTimeoutError as e:
                logging.warning("ERROR getting audio. See below:")
                logging.warning(e)
                pass

            if text:
                logging.debug(f"Recognized text input: {text}")

                new_lang = check_for_translation_change(text)
                if new_lang:
                    TRANSLATE_TO = new_lang
                    logging.debug(f"Switched to {new_lang}")
                
                if (text == "silent") or (text == "stop"):
                    ACTIVE_MODE = False
                if (text == "active") or (text == "start"):
                    ACTIVE_MODE = True
                
                if ACTIVE_MODE:
                    translation = translator.translate(text, dest=TRANSLATE_TO).text
                    logging.debug(f"Translated text: {translation}")

                    logging.debug("Translating text!")
                    tts = gTTS(translation, lang=TRANSLATE_TO)
                    tts.save(".tts.mp3")
                    playsound(".tts.mp3")

    except Exception as e:
        logging.warn(e)
        pass
