import pyaudio
import wave
import requests
import soundfile as sf



def record_wav(seconds, save_path, audio_channels):
    """
    Records a wav file and saves it to `save_path`.

    Parameters
    ----------
    seconds : int
        The duration of the recording in seconds.
    save_path : str
        Where the resulting audio file will be saved.
    audio_channels : int
        Number of audio channels (2 for Pi, 1 for MacBook)

    Returns
    -------
    str
        A copy of the `save_path` parameter, where the file is saved.
    """
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    fs = 4410  # Record at 44100 samples per second

    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=audio_channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    # Initialize array to store frames
    frames = []

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()

    # Terminate the PortAudio interface
    p.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(save_path, 'wb')
    wf.setnchannels(audio_channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return save_path


def asr(audio_file, whisper_server_url):
    """
    Sends an audio file that might contain speech to the whisper server,
    which returns a transcription of any speech it might contain.

    Parameters
    ----------
    recording : str
        The path to an audio file that might contain speech.
    whisper_server_url : str
        Path to the whisper server.
    
    Returns
    -------
    str
        The text that corresponds to the audio file. Might also return empty parens: ""
    """
    data, samplerate = sf.read(audio_file)

    data = {"audio_info": str(data.tolist()), "samplerate": samplerate}

    r = requests.get(whisper_server_url, data=data)

    return eval(r.text)["transcription"]



# For texting on MacBook
if __name__ == "__main__":
    audio_path = record_wav(seconds=10, save_path="_output.wav", audio_channels=1)

    text = asr(audio_path, whisper_server_url="http://192.168.4.157:5000/whisper")

    print(text)
