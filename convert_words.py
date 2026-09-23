"""Decode a PNG made by binToImage.py, or encode the bundled word list as a bulk test.

    python convert_words.py <image.png>        decode and report the character count
    python convert_words.py --encode-wordlist  write words_alpha.txt into wordlist.png
"""
import sys

from binToImage import binToImg, imgToText


def main(argv):
    if argv and argv[0] == "--encode-wordlist":
        with open("words_alpha.txt", encoding="utf-8") as f:
            path = binToImg(f.read(), "wordlist.png")
        print(f"Encoded words_alpha.txt into '{path}'")
        return 0

    path = argv[0] if argv else input("Image Path: ").strip()
    print("Starting...")
    try:
        words = imgToText(path)
    except (FileNotFoundError, ValueError) as exc:
        print(exc)
        return 1
    print(f"{words}\n------------------------------\nNumber of Characters Extracted from '{path}': {len(words)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
