import math
import cv2
from multiprocessing import Pool

availableCharacters = open("characterSets.txt", "r").read().split("\n")

width = None 
image = None

# This function will convert a PIL frame to ascii text
def convertToAsciiTraditional(InImage, cols=120, onSymbol="", offSymbol="", characterSet="default"):
    global asciiValues
    global width
    global image

    image = InImage

    if characterSet != "":
        for set in availableCharacters:
            if set.startswith(characterSet):
                asciiValues = set.split(";")[1]
                break

    if onSymbol != "":
        asciiValues = onSymbol + offSymbol

    # Get the original size
    width, height = image.shape
    # Get the aspect ratios
    aspect = height/width
    # Calculate the new height
    newHeight = int(cols/aspect/2)
    # Resize the image
    image = cv2.resize(image, (cols, newHeight))
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Then re set height and width
    width, height = image.shape

    # Initialize the ascii image
    asciiImage = ""


    # Loop through each row in the image
    for y in range(height-1):
        # Add a border at the start of each row
        asciiImage += "│"
        # Loop through each pixel in the row
        for x in range(width-1, 0, -1):
            # Get the pixel value at (x, y)
            pixel = image[x][y]
            # Get the grayscale value of the pixel
            grayscale = pixel

            # Then clamp that 255 to 69
            index = math.floor(grayscale * (len(asciiValues) - 1) / 255)
            # And invert it
            index = len(asciiValues) - 1 - index

            colorIndex = 232 + math.floor(grayscale * (24-1) / 255)

            # Append the ascii character to the string
            asciiImage += f"\x1b[38;5;{colorIndex}m" + asciiValues[index] + "\x1b[0m"

        # Add a newline and border at the end of each row
        asciiImage += "│\n"

    # Add an extra row of borders at the bottom
    asciiImage += "└"
    for x in range(width-1):
        asciiImage += "─"
    asciiImage += "┘"

    # Return the image back
    return asciiImage


def rgbTo8bit(rgb):
    red = int((rgb[0] * 8) / 256)
    green = int((rgb[1] * 8) / 256)
    blue = int((rgb[2] * 4) / 256)

    return (red << 5) | (green << 2) | blue


# This function will convert a PIL frame to ascii text
def convertToAscii(image, percentage, cols=120, color=False):
    global asciiValues

    # Get the original size
    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    # Get the aspect ratios
    aspect = height/width
    # Calculate the new height
    newHeight = int(cols/aspect/2)
    # Resize the image
    image = cv2.resize(image, (cols, newHeight))
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    # Then re set height and width
    if color:
        width, height, colorDepth = image.shape
    else:
        width, height = image.shape

    # Initialize the ascii image
    asciiImage = ""

    # Loop through each row in the image
    for y in range(height-1):
        # Add a border at the start of each row
        asciiImage += "│"
        # Loop through each pixel in the row
        for x in range(width-1, 0, -1):
            # Get the pixel value at (x, y)
            pixel = image[x][y]
            # Get the grayscale value of the pixel
            # WHY DOES (255+255+255)/3 = 84?????? PYTHON PLZ

            if color:
                index = rgbTo8bit(pixel)
                asciiImage += f"\x1b[38;5;{index}m" + "█" + "\x1b[0m"
                continue    

            grayscale = pixel
            # Clamp the number to the 24 colors
            index = 232 + math.floor(grayscale * (24-1) / 255)

            # Append the ascii character to the string
            asciiImage += f"\x1b[38;5;{index}m" + "█" + "\x1b[0m"

        # Add a newline and border at the end of each row
        asciiImage += "│\n"

    # Add an extra row of borders at the bottom
    asciiImage += "\x1b[38;5;28m" + "└" + "\x1b[0m"
    wasUnder = False
    count = 0
    for x in range(width-1):
        framePercentage = (x / width) * 100
        if framePercentage < percentage:
            # Green ─
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

    # Return the image back
    return asciiImage

