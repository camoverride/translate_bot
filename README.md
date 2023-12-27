# Translate Bot

Translates to a language of your choice!


## Pi Setup

- `git clone https://github.com/camoverride/newlife.git`
- `cd newlife`
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `sudo apt-get install  python3-pyaudio`
- `pip install -r requirements.txt`
- `sudo apt-get install flac`

Suppress annoying "pop-up" noise:
`sudo mv /usr/share/piwiz/srprompt.wav /usr/share/piwiz/srprompt.wav.bak`

Change volume: `alsamixer`


## Run

`nohup python translate_bot.py &`

Stop: `sudo shutdown -h now`


Start a service with *systemd*. This will start the program when the computer starts and revive it when it dies. Copy the contents of `translate_bot.service` to `/etc/systemd/system/translate_bot.service` (via `sudo vim /etc/systemd/system/translate_bot.service`).

Start the service using the commands below:

- `sudo systemctl daemon-reload`
- Start it on boot: `sudo systemctl enable translate_bot.service`
- Start it right now: `sudo systemctl start translate_bot.service`
- Stop it right now: `sudo systemctl stop translate_bot.service`
- Get logs: `sudo journalctl -u translate_bot | tail`


## How to use

The bot listens to your speech and repeats it back, translated into a new language.

To switch languages, simply say "translate Chinese." A full list of languages is in `gtts_lang_codes.py`

Say: "silent", "stop", "quiet", or "turn off" to quiet the transcription.
Say: "active", "start", "speak to me", or "turn on" to start the transcription.
