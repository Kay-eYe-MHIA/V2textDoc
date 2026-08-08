"""Local speech-to-text via faster-whisper. Runs entirely on the machine —
uploaded audio is written to a temp file only for the duration of
transcription, then deleted; nothing is persisted to disk.
"""
import os
import tempfile

from faster_whisper import WhisperModel

WHISPER_MODEL_SIZE = os.environ.get("WHISPER_MODEL_SIZE", "small")
WHISPER_DEVICE = os.environ.get("WHISPER_DEVICE", "cpu")
WHISPER_COMPUTE_TYPE = os.environ.get("WHISPER_COMPUTE_TYPE", "int8")
# "en" by default; set to "ms" for Malay, or blank/unset for auto-detect
# (useful for mixed English/Malay "Manglish" clinical speech).
WHISPER_LANGUAGE = os.environ.get("WHISPER_LANGUAGE", "en") or None

_model: WhisperModel | None = None


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        _model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device=WHISPER_DEVICE,
            compute_type=WHISPER_COMPUTE_TYPE,
        )
    return _model


def transcribe_audio(audio_bytes: bytes, suffix: str = ".webm") -> str:
    model = _get_model()
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(audio_bytes)
        segments, _info = model.transcribe(path, language=WHISPER_LANGUAGE, vad_filter=True)
        return " ".join(segment.text.strip() for segment in segments).strip()
    finally:
        os.remove(path)
