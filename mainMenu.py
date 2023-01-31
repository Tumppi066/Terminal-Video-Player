import os

def Information():
    os.system("cls")

    name = input("""
    ┌─ Video file name (default : video.mp4)
    │
    │  Remember to include the file extension.
    │ 
    ╰─> """)

    if name == "":
        name = "video.mp4"

    os.system("cls")


    show = input("""
    ┌─ Show raw video (default : n)
    │
    │  Will show the full resolution video in a window.
    │ 
    ╰─> """)

    if show == "":
        show = "y"

    os.system("cls")

    fps = input("""
    ┌─ Video fps (default : 30)
    │
    │  This is used to sync the frames correctly.
    │  If the video is playing too slow of fast change this.
    │ 
    ╰─> """)

    if fps == "":
        fps = 30
    else:
        fps = int(fps)

    os.system("cls")

    color = input("""
    ┌─ Color (default : n)
    │
    │  This will print out 8 bit colors
    │
    ╰─> """)

    if color == "":
        color = "n"

    os.system("cls")

    width = input("""
    ┌─ Viewport width (default : 120)
    │
    │  The width of the displayed video.
    │  Higher values require more processing power.
    │ 
    ╰─> """)

    if width == "":
        width = 120
    else:
        width = int(width)

    os.system("cls")

    useTraditional = input("""
    ┌─ Use traditional characters (default : n)
    │
    │  This will use characters to achieve grayscale instead of colors.
    │  This is useful if you are using a font that doesn't support the default characters, or colors.
    │
    ╰─> """)

    if useTraditional == "":
        useTraditional = "n"

    os.system("cls")

    if useTraditional == "y":

        style = input("""
        ┌─ Character style (default : default)
        │
        │  Available styles are : 
        │  default : 70 normal characters
        │  default10 : 10 normal characters (sometimes better)
        │  pixel : 4 pixel characters, sometimes requires additional font
        │  custom : 2 custom characters
        │ 
        ╰─> """)

        if style == "custom":
            global onPixel
            global offPixel
            onPixel = input("""
            ┌─ On pixel character (default : █)
            │
            │  This is the character that will be used to represent a white pixel.
            │ 
            ╰─> """)

            if onPixel == "":
                onPixel = "█"

            offPixel = input("""
            ┌─ Off pixel character (default : ' ')
            │
            │  This is the character that will be used to represent a black pixel.
            │ 
            ╰─> """)

            if offPixel == "":
                offPixel = " "

            style = onPixel + ";" + offPixel

        if style == "":
            style = "default"

    else:
        onPixel = "█"
        offPixel = " "
        style = "default"

    return name, fps, width, style, show, useTraditional, color
