# Kokoro-82M TTS

Small local demo for [`hexgrad/Kokoro-82M`](https://huggingface.co/hexgrad/Kokoro-82M).

## Setup

Kokoro currently supports Python `>=3.10,<3.13`, so use Python 3.12 or 3.11. It also needs the system package `espeak-ng`.

On Ubuntu 26.04, the default `python3` can be too new for Kokoro. Use `uv` to install a compatible Python just for this project:

```bash
sudo apt-get update
sudo apt-get install -y espeak-ng curl
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv python install 3.12
rm -rf .venv
uv venv --python 3.12 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

If your Linux distro has a native Python 3.10, 3.11, or 3.12 package, you can use that instead:

```bash
python3.11 -m venv .venv
```

## Use

```bash
source .venv/bin/activate
python synthesize.py "Kokoro is running locally." -o kokoro.wav
```

Useful options:

```bash
python synthesize.py "Your text here" --voice af_heart --lang-code a --output output.wav
```

The model runs at 24 kHz and writes a WAV file.

## API

Install the API dependencies after updating `requirements.txt`:

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

Start the server:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

Check that it is running:

```bash
curl http://127.0.0.1:8000/health
```

Generate a WAV file:

```bash
curl -X POST http://127.0.0.1:8000/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from the Kokoro API.","voice":"af_heart","lang_code":"a"}' \
  --output speech.wav
```

Stream audio while Kokoro is generating it:

```bash
curl -N -X POST http://127.0.0.1:8000/tts/stream \
  -H "Content-Type: application/json" \
  -d '{"text":"This audio starts downloading while it is generated.","voice":"af_heart","lang_code":"a"}' \
  --output live.wav
```

Use the live endpoint directly in a browser or HTML audio tag:

```text
http://127.0.0.1:8000/tts/live?text=Hello%20from%20live%20Kokoro&voice=af_heart&lang_code=a
```

```html
<audio controls autoplay src="http://127.0.0.1:8000/tts/live?text=Hello%20from%20Kokoro"></audio>
```

Open the interactive API docs in your browser:

```text
http://127.0.0.1:8000/docs
```
