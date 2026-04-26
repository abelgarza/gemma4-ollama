from __future__ import annotations

import base64
from pathlib import Path

import pytest
from gemma4_ollama.audio import read_wav_as_base64, wav_to_base64


def test_imports():
    """Verify that the package can be imported and exports expected symbols."""
    assert wav_to_base64 is not None
    assert read_wav_as_base64 is not None
    assert wav_to_base64 == read_wav_as_base64


def test_wav_validation_fails_on_invalid_header(tmp_path: Path):
    """Verify that wav_to_base64 raises ValueError for non-WAV files."""
    invalid_file = tmp_path / "test.txt"
    invalid_file.write_text("not a wav file")
    
    with pytest.raises(ValueError, match="Expected WAV file"):
        wav_to_base64(invalid_file)


def test_wav_to_base64_with_sample():
    """Verify wav_to_base64 with the project's sample audio."""
    sample_path = Path("data/sample-audio/sample.wav")
    if not sample_path.exists():
        pytest.skip("Sample audio file not found")
        
    result = wav_to_base64(sample_path)
    assert isinstance(result, str)
    # Basic check if it's valid base64
    decoded = base64.b64decode(result)
    assert decoded[:4] == b"RIFF"
    assert decoded[8:12] == b"WAVE"


def test_mock_wav(tmp_path: Path):
    """Verify wav_to_base64 with a minimal valid-header mock WAV."""
    mock_wav = tmp_path / "mock.wav"
    # Minimal RIFF WAVE header
    header = b"RIFF" + b"\x00" * 4 + b"WAVE" + b"fmt " + b"\x00" * 20
    mock_wav.write_bytes(header)
    
    result = wav_to_base64(mock_wav)
    decoded = base64.b64decode(result)
    assert decoded.startswith(b"RIFF")
    assert b"WAVE" in decoded[:12]
