"""HTTP API for Kokoro TTS."""

from __future__ import annotations

from io import BytesIO
from collections.abc import Iterator
import struct

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel, Field

from tts_engine import SAMPLE_RATE, synthesize_audio, synthesize_chunks

app = FastAPI(title="Kokoro TTS API")


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    voice: str = "af_heart"
    lang_code: str = "a"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tts")
def text_to_speech(request: TTSRequest) -> Response:
    try:
        audio = synthesize_audio(
            text=request.text,
            voice=request.voice,
            lang_code=request.lang_code,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    wav = BytesIO()
    sf.write(wav, audio, SAMPLE_RATE, format="WAV")
    wav.seek(0)

    return Response(
        content=wav.read(),
        media_type="audio/wav",
        headers={"Content-Disposition": 'attachment; filename="speech.wav"'},
    )


def wav_stream_header(sample_rate: int) -> bytes:
    data_size = 0  # Unknown size for streaming
    riff_size = 0  # Unknown size for streaming
    byte_rate = sample_rate * 2
    block_align = 2

    return struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",
        riff_size,
        b"WAVE",
        b"fmt ",
        16,
        1,
        1,
        sample_rate,
        byte_rate,
        block_align,
        16,
        b"data",
        data_size,
    )


def pcm16_bytes(audio: np.ndarray) -> bytes:
    if hasattr(audio, "numpy"):
        audio = audio.cpu().numpy()
    clipped = np.clip(audio, -1.0, 1.0)
    return (clipped * 32767).astype("<i2").tobytes()


def stream_wav_chunks(request: TTSRequest) -> Iterator[bytes]:
    yield wav_stream_header(SAMPLE_RATE)

    for audio in synthesize_chunks(
        text=request.text,
        voice=request.voice,
        lang_code=request.lang_code,
    ):
        yield pcm16_bytes(audio)


@app.post("/tts/stream")
def stream_text_to_speech(request: TTSRequest) -> StreamingResponse:
    return StreamingResponse(
        stream_wav_chunks(request),
        media_type="audio/wav",
        headers={"Content-Disposition": 'inline; filename="speech-stream.wav"'},
    )


@app.get("/tts/live")
def live_text_to_speech(
    text: str,
    voice: str = "af_heart",
    lang_code: str = "a",
) -> StreamingResponse:
    request = TTSRequest(text=text, voice=voice, lang_code=lang_code)
    return stream_text_to_speech(request)
