"""Shared Kokoro TTS generation helpers."""

from __future__ import annotations

from functools import lru_cache
from collections.abc import Iterator

import numpy as np
from kokoro import KPipeline

SAMPLE_RATE = 24000


@lru_cache(maxsize=8)
def get_pipeline(lang_code: str) -> KPipeline:
    return KPipeline(lang_code=lang_code)


def synthesize_chunks(
    text: str,
    voice: str = "af_heart",
    lang_code: str = "a",
) -> Iterator[np.ndarray]:
    pipeline = get_pipeline(lang_code)

    for _, _, audio in pipeline(text, voice=voice):
        yield audio


def synthesize_audio(text: str, voice: str = "af_heart", lang_code: str = "a") -> np.ndarray:
    chunks = []

    for audio in synthesize_chunks(text, voice=voice, lang_code=lang_code):
        chunks.append(audio)

    if not chunks:
        raise RuntimeError("Kokoro did not generate any audio chunks.")

    if len(chunks) == 1:
        return chunks[0]

    return np.concatenate(chunks)
