# Transmissions

Prints out your speech.


## Pi Setup

- `git clone git@github.com:camoverride/translate_bot.git`
- `cd translate_bot`
- `python -m venv .venv`
- `source .venv/bin/activate`
- `sudo apt-get install portaudio19-dev`
- `pip install -r requirements.txt`
- `sudo apt-get install flac`

Printer setup:
- `sudo apt install libatlas-base-dev libgstreamer1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good libcups2-dev libcupsimage2-dev git build-essential cups system-config-printer`
- `git clone https://github.com/adafruit/zj-58`
- `cd zj-58`
- `make`
- `sudo ./install`
- `lpadmin -p text_printer -v usb://POS58/Printer?serial=FMD072`
- `lpadmin -p text_printer -E -m zjiang/ZJ-58.ppd`
- `sudo lp -d text_printer test_image.png`

Suppress annoying "pop-up" noise:
`sudo mv /usr/share/piwiz/srprompt.wav /usr/share/piwiz/srprompt.wav.bak`

Suppress jack debug:
`sudo apt-get install jackd`
`jack_control start`

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

To quiet the transcription, say: "silent", "stop", "quiet", or "turn off."
To activate the transcription, say: "active", "start", "speak to me", or "turn on."

Play with the global settings in `translate_bot.py`
