# bmw-assist-project-v2

ChatGPT based voice assistant with car computer integrations.

Speech is captured from the microphone, processed through OpenAI, converted to
speech with Google TTS, and played back — while a KITT-style LED voice module
(3×20 LED bar graphs driven over GPIO) visualises the loudness of the response
in real time.

## Running

```bash
make -C assist/assistant/screen      # build the GPIO driver (once)
source venv/bin/activate
set -a && source .env && set +a
cd assistant
python main.py
```

Run as your normal user (no `sudo`). The user must be in the `gpio` and `audio`
groups so the LED driver and audio playback share one process.
