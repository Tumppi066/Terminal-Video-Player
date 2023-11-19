import math
import cv2
import numpy as np

availableCharacters = open("characterSets.txt", "r", encoding="utf-8").read().split("\n")

width = None 
image = None

asciiValues = availableCharacters[-1]
# Reverse the string
asciiValues = asciiValues[::-1]
asciiLen = len(asciiValues)

print("Precomputing values...")
pixelIndexes = []
for x in range(256):
    grayscale = x
    index = int(round(grayscale/255*(asciiLen-1), 0))
    pixelIndexes.append(index)
pixel_indexes = np.array(pixelIndexes)

# RGB array for the color tag strings
colorPixels = np.empty((256, 256, 256), dtype=object)
for r in range(256):
    for g in range(256):
        for b in range(256):
            colorPixels[r, g, b] = f"\x1b[38;2;{r};{g};{b}m█"


# This function will convert a PIL frame to ascii text
def convertToAscii(image, percentage, cols=120, color=False):
    localValues = asciiValues
    localPixelIndices = pixelIndexes

    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    aspect = height/width
    newHeight = int(cols/aspect/2)
    image = cv2.resize(image, (cols, newHeight))

    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    
    # Convert grayscale image to indexes directly using NumPy
    if not color:
        indices = np.round(image.flatten() / 255 * (asciiLen - 1)).astype(int)
        ascii_chars = np.array(list(asciiValues))[indices]  # Map indices to ASCII characters
        asciiImage = [''.join(ascii_chars[i:i+cols]) for i in range(0, len(ascii_chars), cols)]

        return "\n".join(asciiImage)
    

    colorImage = colorPixels[image[..., 0], image[..., 1], image[..., 2]]

    asciiImage = []
    lastColor = None
    for row in colorImage:
        line = ""
        for color in row:
            if color != lastColor:
                line += "\x1b[0m" + color
                lastColor = color
            else:
                line += "█"
        asciiImage.append(line + "\n")

    asciiImage = ''.join(asciiImage)
    asciiImage += "\x1b[38;5;28m" + "└" + "\x1b[0m"
    
    wasUnder = False
    count = 0
    for x in range(height-1):
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