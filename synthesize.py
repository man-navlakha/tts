#!/usr/bin/env python3
"""Generate speech with hexgrad/Kokoro-82M."""

from __future__ import annotations

import argparse
from pathlib import Path

import soundfile as sf

from tts_engine import SAMPLE_RATE, synthesize_audio


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a WAV file with Kokoro TTS.")
    parser.add_argument("text", nargs="?", default="Hello from Kokoro text to speech.")
    parser.add_argument("-o", "--output", default="output.wav", help="Output WAV path.")
    parser.add_argument("-v", "--voice", default="af_heart", help="Voice name, e.g. af_heart.")
    parser.add_argument(
        "-l",
        "--lang-code",
        default="a",
        help="Kokoro language code. Use 'a' for American English.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    audio = synthesize_audio(args.text, voice=args.voice, lang_code=args.lang_code)
    sf.write(output, audio, SAMPLE_RATE)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
