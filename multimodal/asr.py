import tempfile
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(audio_bytes.getvalue())
        audio_path = f.name

    segments, _ = model.transcribe(audio_path)
    text = " ".join([seg.text for seg in segments])

    confidence = 0.9 if text.strip() else 0.3
    return text.strip(), confidence
