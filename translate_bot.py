from datetime import datetime
import logging
import os



# Global settings
ACTIVE_MODE = True
ASR_METHOD = "whisper" # "google"
WHISPER_RECORDING_DURATION = 10
AUDIO_CHANNELS = 2
WHISPER_SERVER_URL = "http://192.168.4.157:5000/whisper"

# Logging
logging.basicConfig(level=logging.WARNING)

# Imports based on ASR type
if ASR_METHOD == "whisper":
    from whisper_utils import record_wav, asr
elif ASR_METHOD == "google":
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False # stop mic from recording ambient noise

# Suppress horrible Alsa debug
from ctypes import *
from contextlib import contextmanager
import pyaudio

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

# Suppress Jack server warning
os.system("jack_control start")

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)



# Main event loop
while True:
    if ASR_METHOD == "google":
        logging.warning(f"Function started at: {datetime.now()}")
        logging.warning(f"Speaking mode on:    {ACTIVE_MODE}")
        logging.warning(f"")
        try: # The main loop always continues!
            with noalsaerr() as _, sr.Microphone() as source:
                text = None

                try:
                    # Get Audio clip
                    logging.warning("> Getting audio")
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                    # Speech-to-text
                    logging.warning("> Speech to text")
                    try:
                        text = recognizer.recognize_google(audio, language="en-us")
                    except sr.exceptions.UnknownValueError as e:
                        logging.warning("ERROR: Speech not understood")
                        pass

                except sr.exceptions.WaitTimeoutError as e:
                    logging.warning("No speech recorded")
                    pass

                if text:
                    logging.warning(f"[Google] recognized text input:  {text}")

                    if text in ["silent", "stop", "quiet", "turn off"]:
                        ACTIVE_MODE = False
                    if text in ["active", "start", "speak to me", "turn on"]:
                        ACTIVE_MODE = True
                    
                    if ACTIVE_MODE:
                        # Print text
                        os.system("sudo chmod 777 /dev/usb/lp0")
                        os.system(f'echo "{text}\\n" > /dev/usb/lp0')

        except Exception as e:
            logging.warning(e)
            pass


    elif ASR_METHOD == "whisper":
        audio_path = record_wav(seconds=WHISPER_RECORDING_DURATION,
                                save_path="_output.wav",
                                audio_channels=AUDIO_CHANNELS)

        text = asr(audio_path, whisper_server_url=WHISPER_SERVER_URL)

        if text:
            logging.warning(f"[Whisper] recognized text input:  {text}")

            if text in ["silent", "stop", "quiet", "turn off"]:
                ACTIVE_MODE = False
            if text in ["active", "start", "speak to me", "turn on"]:
                ACTIVE_MODE = True
            
            if ACTIVE_MODE:
                # Print text
                os.system("sudo chmod 777 /dev/usb/lp0")
                os.system(f'echo "{text}\\n" > /dev/usb/lp0')

    
    logging.warning("--------------------------------------")
