<div align="center">

# MessageInPicture

**Write text into the pixels of an image, then read it back out.**

Every character becomes 8 bits, every bit becomes one pixel: black for `0`, white for `1`. The result is a lossless PNG that *is* the message rather than a picture hiding one.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white)

</div>

---

## How it works

```
"Hi"  ->  01001000 01101001         text to bits (8 per character)
      ->  [0,1,0,0,1,0,0,0,...]     flat bit array
      ->  reshaped to ~sqrt(n) rows  squarest grid that fits
      ->  x255                       1 becomes white, 0 stays black
      ->  binary_image.png           PNG, compression level 0
```

Decoding runs the same path backwards: read greyscale, threshold at 127, flatten, regroup into bytes, decode UTF-8.

The grid is sized to `rows = floor(sqrt(bits))`, so the image comes out roughly square regardless of message length.

---

## Two things that matter

**Compression must be off.** The PNG is written with `IMWRITE_PNG_COMPRESSION = 0`. Every pixel carries one bit, so a lossy or resampling step does not soften the image, it corrupts the payload.

**This is encoding, not steganography.** There is no cover image and nothing is hidden. Anyone looking at the file sees noise and can decode it with the same script. It is a visual representation of bytes, not a way to conceal them.

---

## Usage

```bash
pip install opencv-python numpy
python binToImage.py
```

You get a prompt:

```
What would you like to do:
i)  Convert text to Image
ii) Convert Image to Text
```

`convert_words.py` is the batch path: point it at a PNG and it decodes and reports the character count. The commented block at the top encodes `words_alpha.txt` instead, which is what the 4MB English wordlist in this repo is for. It makes a large, dense test image.

---

## Files

| File | Purpose |
|---|---|
| `binToImage.py` | `binToImg`, `imgToBin`, `binToStr`, plus the interactive menu |
| `convert_words.py` | Decode a PNG to text, or encode the wordlist |
| `words_alpha.txt` | ~370k English words, used as a bulk test payload |
| `binary_image.png` | Sample output |

---

<sub>An early experiment. Kept for the idea rather than the code.</sub>
