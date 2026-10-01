import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from binToImage import binToImg, binToStr, imgToBin, imgToText  # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")


@pytest.mark.parametrize("message", [
    "Hi",
    "Hello, world!",                # not a square number of bits
    "line one\nline two\n\tindented",
    "naïve café ✓ नमस्ते 🙂",       # non-ASCII and multi-byte UTF-8
    "x" * 5000,
])
def test_round_trip_is_lossless(tmp_path, message):
    path = binToImg(message, str(tmp_path / "msg.png"))
    assert imgToText(path) == message


def test_empty_message_is_rejected(tmp_path):
    with pytest.raises(ValueError):
        binToImg("", str(tmp_path / "empty.png"))


def test_missing_image_raises_a_clear_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        imgToBin(str(tmp_path / "nope.png"))


def test_non_text_payload_raises_value_error():
    with pytest.raises(ValueError):
        binToStr("11111111" * 4)  # 0xFF bytes are not valid UTF-8


def test_bundled_sample_still_decodes():
    text = imgToText(os.path.join(ROOT, "binary_image.png"))
    assert text.startswith("Hello") and "Muneer" in text
    assert not text.endswith("\x00")
