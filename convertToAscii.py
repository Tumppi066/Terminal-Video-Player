import math
import cv2
from multiprocessing import Pool

availableCharacters = open("characterSets.txt", "r", encoding="utf-8").read().split("\n")

width = None 
image = None

asciiValues = availableCharacters[-1]
# Reverse the string
asciiValues = asciiValues[::-1]
asciiLen = len(asciiValues)

# This function will convert a PIL frame to ascii text
def convertToAscii(image, percentage, cols=120, color=False):
    global asciiValues

    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    aspect = height/width
    newHeight = int(cols/aspect/2)
    image = cv2.resize(image, (cols, newHeight))
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    asciiImage = []
    lastPixel = [-1,-1,-1] if color else -1
    lastChar = ""

    pixelIndexes = []
    if not color:
        for x in range(256):
            grayscale = x
            index = int(round(grayscale/255*(asciiLen-1), 0))
            pixelIndexes.append(index)

    skip = 0
    for y in range(height-1):
        row = ["│"]
        for x in range(width-1, 0, -1):
            if skip > 0:
                skip -= 1
                continue
            
            pixel = image[x][y]

            if color:
                if pixel[0] == lastPixel[0] and pixel[1] == lastPixel[1] and pixel[2] == lastPixel[2]:
                    row[-1] = row[-1][:-4] + "█" + "\x1b[0m"
                    continue
            else:
                if pixel == lastPixel:
                    row.append(lastChar)
                    continue

            if color:
                lastChar = f"\x1b[38;2;{pixel[0]};{pixel[1]};{pixel[2]}m█\x1b[0m"
                row.append(lastChar)
                lastPixel = pixel
                continue    

            else:
                grayscale = pixel
                index = int(pixelIndexes[grayscale])
                row.append(asciiValues[index])
                lastPixel = pixel
                lastChar = asciiValues[index]

        row.append("│\n")
        asciiImage.append(''.join(row))
        lastChar = ""
        lastPixel = [-1,-1,-1] if color else -1

    asciiImage = ''.join(asciiImage).replace("\uFFFD", "")

    asciiImage += "\x1b[38;5;28m" + "└" + "\x1b[0m"
    wasUnder = False
    count = 0
    for x in range(width-1):
        framePercentage = (x / width) * 100
        if framePercentage < percentage:
            asciiImage += "\x1b[38;5;28m" + "─" + "\x1b[0m"
            wasUnder = True
            count += 1
        elif wasUnder:
            asciiImage += "\x1b[38;5;28m" + "┬" + "\x1b[0m"
            wasUnder = False
        else:
            asciiImage += "─"

    if percentage > 99:
        asciiImage += "\x1b[38;5;28m" + "┤" + "\x1b[0m"
    else:
        asciiImage += "┘"
    asciiImage += "\n\x1b[38;5;28m" + " " * (count - 1) + format(percentage, ".2f") + "%\x1b[0m"

    return asciiImage