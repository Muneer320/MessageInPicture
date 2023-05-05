from binToImage import *

# f = open("words_alpha.txt", "r")
# print("To end please press CTLR+Z and hit Enter.")
# binToImg(f.read())
# print("Image saved at 'binary_image.png'")
# f.close()

path = input("Image Path: ")
print("Starting...")
Words = binToStr(imgToBin(path))
print(f"{Words}\n------------------------------\nNumber of Characters Extracted from '{path}': {len(Words)}")
