from __future__ import annotations

import base64
from pathlib import Path

import pytest
from gemma4_ollama.audio import audio_to_base64


def test_imports():
    """Verify that the package can be imported and exports expected symbols."""
    assert audio_to_base64 is not None


def test_audio_validation_fails_on_invalid_header(tmp_path: Path):
    """Verify that audio_to_base64 raises ValueError for non-audio files."""
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("not an audio file")
    
    with pytest.raises(ValueError, match="Expected audio file"):
        audio_to_base64(invalid_file)


def test_audio_to_base64_with_sample_wav():
    """Verify audio_to_base64 with the project's sample WAV audio."""
    sample_path = Path("data/sample-audio/sample.wav")
    if not sample_path.exists():
        pytest.skip("Sample WAV audio file not found")
        
    result = audio_to_base64(sample_path)
    assert isinstance(result, str)
    # Basic check if it's valid base64
    decoded = base64.b64decode(result)
    assert decoded[:4] == b"RIFF"
    assert decoded[8:12] == b"WAVE"


def test_audio_to_base64_with_sample_mp3():
    """Verify audio_to_base64 with the project's sample MP3 audio."""
    sample_path = Path("data/sample-audio/sample-earnings.mp3")
    if not sample_path.exists():
        pytest.skip("Sample MP3 audio file not found")
        
    result = audio_to_base64(sample_path)
    assert isinstance(result, str)
    # Basic check if it's valid base64
    decoded = base64.b64decode(result)
    # The new implementation converts everything to WAV
    assert decoded[:4] == b"RIFF"
    assert decoded[8:12] == b"WAVE"


def test_mock_wav_fails(tmp_path: Path):
    """Verify audio_to_base64 fails with a minimal mock WAV since ffmpeg does actual validation."""
    mock_wav = tmp_path / "mock.wav"
    # Minimal RIFF WAVE header but no valid audio stream
    header = b"RIFF" + b"\x00" * 4 + b"WAVE" + b"fmt " + b"\x00" * 20
    mock_wav.write_bytes(header)
    
    with pytest.raises(ValueError, match="Expected audio file"):
        audio_to_base64(mock_wav)
