# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# RULES TO ALWAYS FOLLOW

You are an expert senior python developer. The goal of this project is to create a simplistic, clean and meaningful architecture design.
* Never comment code, unless absolutely nescessary
* Be very strict. Add maximum of 10 lines at a time. Whole features shouldn't be longer than 10-15 lines.
* Explain why your short codebase changes are good design to the user after each session - but keep the code changes minimal
* Before doing, read the codebase and stay in the pattern
* This is meant to be a showroom project. Not only made to work, but the code should be structured and beautifull enough to be hanged on a wall in a frame.
* Ask when hesitant, say when in doubt and don't flip the table if unsure. Explain your doubts instead, or explore more deeply once again.

## Project Overview

**bmw-assist-project-v2** is a ChatGPT-based voice assistant with car computer integrations. The application uses speech recognition to capture voice commands, processes them through OpenAI's API, converts responses to speech using Google TTS, and plays audio back to the user.

## Architecture

The application follows a pipeline architecture with three main concurrent processes that communicate via async queues:

1. **Audio Input Pipeline**: `Gatherer` uses `speech_recognition` to capture voice input from the microphone and convert it to text using Google's speech recognition API (Polish language support).

2. **Text Processing Pipeline**: `TextProcessor` (abstract base) with `ChatGPT` implementation sends prompts to OpenAI's API and streams responses back. The implementation:
   - Uses OpenAI's streaming API (`gpt-3.5-turbo`)
   - Buffers streamed content and splits on sentence terminators (`.!?`)
   - Places complete sentences into a `TextQueue` to enable parallel processing
   - Sends `None` sentinel to signal completion

3. **Text-to-Speech & Audio Output Pipeline**: 
   - `google_tts` coroutine consumes from `TextQueue`, generates audio using gTTS (Google Text-to-Speech)
   - Converts generated MP3 to `AudioSegment` objects via pydub
   - Places audio segments into `AudioQueue`
   - `AudioProcessor` consumes from `AudioQueue` and plays audio via `play_simpleaudio` (which uses simpleaudio library)
   - While each segment plays, `AudioProcessor` concurrently drives an optional `Visualizer` (`asyncio.gather`), so both are paced by wall-clock time and stay in sync.

4. **GPIO Voice Module (KITT visualizer)**: a 3×20 LED bar-graph display that lights up with the loudness of the spoken response.
   - `screen.cpp` is a C++ driver compiled to `libscreen.so`. It `mmap`s `/dev/gpiomem` (BCM2711 registers — no root, no PWM, plain on/off) and runs an 800 Hz multiplexing loop in a background `std::thread`, lighting one bar graph at a time. It exposes a tiny `extern "C"` ABI (`screen_open/write/clear/close`).
   - `Screen` (`screen/driver.py`) is a `ctypes` wrapper giving a fluent `screen.pixel(x, y).on()` interface; it is a context manager that opens/closes the device.
   - `Visualizer` (`screen/visualizer.py`) defines the loudness → matrix mapping in pure Python. Each bar grows symmetrically from the center; side rows carry a `+4` sensitivity offset (`OFFSETS = (4, 0, 4)`) so they light later and lag the middle bar — the KITT effect. `show()` walks an `AudioSegment` in real-time 50 ms windows, rendering `window.max / window.max_possible_amplitude` as the fill.

5. **Main Orchestration**: `Assistant` class coordinates the text/TTS/audio pipelines using `asyncio.gather()` to run them concurrently, enabling streaming responses where text is being generated and converted to speech while still being received from the LLM. `main` wraps a `Screen` and injects a `Visualizer` into the `AudioProcessor`.

### Data Flow

```
Gatherer (speech recognition)
         ↓
    command (str)
         ↓
Assistant.respond(command)
  ├─ TextProcessor.ask(command, text_queue)  [LLM processing]
  ├─ google_tts(text_queue, audio_queue)     [TTS conversion]
  └─ AudioProcessor.play_audio(audio_queue)  [Audio playback]
       ├─ play_simpleaudio(segment)          [speaker]
       └─ Visualizer.show(segment)           [GPIO LED bars]
```

### Queue Types

Custom queue types defined in `assist/assistant/types.py`:
- `TextQueue`: `asyncio.Queue[str | None]` - carries sentences or None sentinel
- `AudioQueue`: `asyncio.Queue[AudioSegment | None]` - carries audio segments or None sentinel

### Running the Application
```bash
make -C assist/assistant/screen      # build libscreen.so (once, or after editing screen.cpp)
source venv/bin/activate
set -a && source .env && set +a
cd assistant
python main.py
```

Run as a normal user (no `sudo`) who is in the `gpio` and `audio` groups: the GPIO
driver reaches `/dev/gpiomem` without root, and audio playback uses the user's
audio session — both in the same process. Running as root breaks audio playback.

Remember to follow the rules defined in "RULES TO ALWAYS FOLLOW" paragraph. It is upmost important.