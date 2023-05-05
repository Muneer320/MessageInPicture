import numpy as np
import cv2


def binToImg(bin):
    # Binary data to convert
    binary_data = ''.join(format(ord(char), '08b') for char in bin)

    # Calculate the image dimensions needed to fit the binary data
    num_elements = len(binary_data)
    num_rows = int(np.sqrt(num_elements))
    num_cols = int(np.ceil(num_elements / num_rows))

    # Reshape the binary data to match the image dimensions
    binary_array = np.array([int(x) for x in binary_data])
    binary_array.resize((num_rows, num_cols))

    # Scale the array to 255 (white) and 0 (black)
    image_array = binary_array * 255

    # Convert the array to an image
    image = np.array(image_array, dtype=np.uint8)

    # Save the image in PNG format
    cv2.imwrite("binary_image.png", image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    print("Done!")

def imgToBin(img_path="binary_image.png"):
    # Load the image
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Threshold the image to create a binary image
    ret, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

    # Flatten the binary image into a 1D array
    binary_array = binary_image.flatten()

    # Convert the binary array to a string
    binary_data = ''.join(str(x) for x in binary_array).replace("255","1")

    # Print the binary string
    return binary_data

def binToStr(binary_data):
    byte_chunks = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

    # Convert each byte chunk to its corresponding integer value
    int_chunks = [int(chunk, 2) for chunk in byte_chunks]

    # Convert the integer chunks to bytes
    byte_data = bytearray(int_chunks)

    # Convert the byte data to a string
    string_data = byte_data.decode('utf-8')
    return string_data

def main():
    inp = input("What would you like to do:\ni) Convert text to Image\nii) Convert Image to Text\nPLEASE ONLY RESPOND IN 'i' OR 'ii'\n>>> ")
    if inp == 'i':
        contents = []
        print("To end please press CTLR+Z and hit Enter.")
        while True:
            try:
                line = input(">>> ")
            except EOFError:
                break
            contents.append(line)
        binToImg('\n'.join(contents))
        bin = imgToBin("binary_image.png")
        print("Image saved at 'binary_image.png'")
        input()
    elif inp == 'ii':
        loc = input("Please enter the image path to be converted. (leave blank for default image path i.e. 'binary_image.png') >>> ").replace("","binary_image.png")
        bin = imgToBin(loc)
        s = binToStr(bin)
        print("Binary value:\n", bin)
        print("--------------------------------")
        print(f"String length: {s}\nString Value: {s}")
        input()
    else:
        print("Please select a valid input.\n\n")
        main()

if __name__=='__main__':
    main()

