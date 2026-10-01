import numpy as np
import cv2

DEFAULT_IMAGE = "binary_image.png"


def binToImg(text, out_path=DEFAULT_IMAGE):
    """Write text into a black/white PNG, one bit per pixel. Returns the output path."""
    data = text.encode('utf-8')
    if not data:
        raise ValueError("Nothing to encode: the message is empty")

    # Text to bits, 8 per byte (UTF-8, so any character works)
    binary_data = ''.join(format(byte, '08b') for byte in data)

    # Squarest grid that fits the bits
    num_elements = len(binary_data)
    num_rows = max(1, int(np.sqrt(num_elements)))
    num_cols = int(np.ceil(num_elements / num_rows))

    # Pad the leftover cells with 0 bits. Padding decodes to NUL bytes, which
    # imgToText strips. np.resize would repeat the data and corrupt the message.
    bits = np.zeros(num_rows * num_cols, dtype=np.uint8)
    bits[:num_elements] = [int(x) for x in binary_data]

    # 1 becomes white (255), 0 stays black
    image = (bits.reshape((num_rows, num_cols)) * 255).astype(np.uint8)

    # Compression level 0: every pixel carries one bit
    if not cv2.imwrite(out_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 0]):
        raise OSError(f"Could not write image to {out_path}")
    return out_path


def imgToBin(img_path=DEFAULT_IMAGE):
    """Read an image and return its pixels as a string of '0'/'1' bits."""
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise FileNotFoundError(f"Could not read an image from '{img_path}'")

    # Threshold at 127: anything bright is a 1
    _, binary_image = cv2.threshold(image, 127, 1, cv2.THRESH_BINARY)
    return ''.join(str(x) for x in binary_image.flatten())


def binToStr(binary_data):
    """Turn a bit string back into text. Trailing padding (NUL bytes) is removed."""
    usable = len(binary_data) - len(binary_data) % 8
    byte_data = bytes(int(binary_data[i:i + 8], 2) for i in range(0, usable, 8))
    try:
        return byte_data.rstrip(b'\x00').decode('utf-8')
    except UnicodeDecodeError as exc:
        raise ValueError("The image does not contain UTF-8 text encoded by this tool") from exc


def imgToText(img_path=DEFAULT_IMAGE):
    return binToStr(imgToBin(img_path))


def main():
    inp = input("What would you like to do:\ni) Convert text to Image\nii) Convert Image to Text\nPLEASE ONLY RESPOND IN 'i' OR 'ii'\n>>> ").strip()
    if inp == 'i':
        contents = []
        print("Type your message. To finish, press Ctrl+Z then Enter (Windows) or Ctrl+D (macOS/Linux).")
        while True:
            try:
                line = input(">>> ")
            except EOFError:
                break
            contents.append(line)
        try:
            path = binToImg('\n'.join(contents))
        except ValueError as exc:
            print(exc)
            return
        print(f"Image saved at '{path}'")
    elif inp == 'ii':
        loc = input(f"Image path (leave blank for '{DEFAULT_IMAGE}') >>> ").strip() or DEFAULT_IMAGE
        try:
            bits = imgToBin(loc)
            text = binToStr(bits)
        except (FileNotFoundError, ValueError) as exc:
            print(exc)
            return
        print("Binary value:\n", bits)
        print("--------------------------------")
        print(f"String length: {len(text)}\nString Value: {text}")
    else:
        print("Please select a valid input.\n")
        main()


if __name__ == '__main__':
    main()
    input("\nPress Enter to exit...")
