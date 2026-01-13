import whisper
import tempfile
import os
import subprocess
import shutil

# 🔴 ABSOLUTE PATH TO FFMPEG.EXE (VERIFY THIS EXISTS)
FFMPEG_EXE = r"C:\Users\saiki\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

# ✅ 1. Verify ffmpeg.exe exists
if not os.path.exists(FFMPEG_EXE):
    raise FileNotFoundError(f"ffmpeg.exe not found at: {FFMPEG_EXE}")

# ✅ 2. Inject ffmpeg directory into PATH (CRITICAL)
ffmpeg_dir = os.path.dirname(FFMPEG_EXE)
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

# ✅ 3. Force Whisper to see ffmpeg via shutil
assert shutil.which("ffmpeg") is not None, "ffmpeg still not visible to Python"

# Load Whisper model
model = whisper.load_model("base")

def transcribe_audio(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(audio_bytes.getvalue())
        audio_path = tmp.name

    result = model.transcribe(
        audio_path,
        fp16=False
    )

    text = result.get("text", "").strip()
    confidence = 0.8 if text else 0.0

    return text, confidence
