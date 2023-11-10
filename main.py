# -*- coding: utf-8 -*-
import cv2 # CV2 Is used to read the video file
import time # Time is used to sync the frames correctly
from convertToAscii import convertToAscii # Import the convertToAscii function
import os # OS is used to clear the console
import mainMenu as menu # Import the main menu
import sys
import codecs
import keyboard
import difflib

# Ask the user for the video file name, fps and width
video, fps, width, style, show, useTraditional, color = menu.Information()


# If the style is custom, parse the characters
if ";" in style:
    onPixel = style.split(";")[0]
    offPixel = style.split(";")[1]
    style = "custom"


# Read the video
video = cv2.VideoCapture(video)
success, img = video.read()

# Initialize variables
frameNumber = 1
Fps = 0
skippedFrames = 1

# Calculate the video length
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
startTime = time.time()

framesLastSecond = 0
lastSecondTime = time.time()

inputTimer = time.time()
inputPadding = 0.1 # seconds

paused = False

offset = 0

startPause = 0
endPause = 0

lastFrame = None

lastSecondFPSs = [0,0,0,0]

while True:

    # Detect left and right keypresses to skip / revind 5s of the video
    if keyboard.is_pressed("left") and inputTimer + inputPadding < time.time():
        offset -= .5


    if keyboard.is_pressed("right") and inputTimer + inputPadding < time.time():
        offset += .5


    video.set(cv2.CAP_PROP_POS_FRAMES, frameNumber)


    # Detect the up and down keypresses to increase / decrease the width
    if keyboard.is_pressed("up") and inputTimer + inputPadding < time.time():
        width += 5
        inputTimer = time.time()
        
    if keyboard.is_pressed("down") and inputTimer + inputPadding < time.time():
        width -= 5
        inputTimer = time.time()
        
    # Detect the space keypress to pause / play the video
    if keyboard.is_pressed("space") and inputTimer + inputPadding < time.time():
        paused = not paused
        inputTimer = time.time()
        print("Paused" if paused else "Playing")
        
    # If we press esc quit
    if keyboard.is_pressed("esc"):
        break
        
    # Use r to reset back to frame 1 (and pause the video)
    if keyboard.is_pressed("r"):
        frameNumber = 1
        offset = 0
        paused = True
        
    if paused:
        # Lower the offset to compensate for the time we are paused
        if startPause == 0:
            startPause = time.time()
        continue    
    else:
        if startPause != 0:
            endPause = time.time()
            offset -= endPause - startPause
            startPause = 0
            endPause = 0

    # Read the next video frame and increment the frame number
    success, img = video.read()
    frameNumber += 1
    
    if frameNumber == 0:
        frameNumber = 1

    
    # If the video is over, break the loop
    if(success == False): 
        os.system("cls" if os.name == "nt" else "clear")
        print("> Video file not found / video ended")
        break
    
    
    # Print the current time
    extraInfo = f"┌ Frame: {frameNumber}/{length} | {format(round(frameNumber/fps, 2), '.2f')}s | "
    # - Frame number
    percentage = round(frameNumber/length*100, 2)
    extraInfo += f"{format(percentage, '.2f')}% | "
    # - Skipped frames
    extraInfo += f"\033[91m{skippedFrames} ({format(round(skippedFrames/frameNumber*100, 2), '.2f')}%) skipped frames\033[97m)"
    # - FPS
    extraInfo += f" | FPS: {format(round(Fps, 0), '.0f')} "
    # Print the controls
    extraInfo += f" | Use ESC to exit (arrow keys for control) "
    # Merge extra info with
    # the box characters
    
    

    # Convert to B&W
    if color == "n":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if(show == "y"):
            cv2.imshow("Video", img)
    else:
        if(show == "y"):
            cv2.imshow("Video", img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    
    # Convert the current video frame to ASCII
    convertTimeStart = time.time()
    if color == "y":
        img = convertToAscii(img, percentage, width, color=True)
    else:
        img = convertToAscii(img, percentage, width)
    convertTimeEnd = time.time()
    
    writeTimeStart = time.time()
    # Clear the console and print the current frame
    if lastFrame is None:
        sys.stdout.write("\033[0;0H")
        sys.stdout.write(extraInfo + "\n")
        sys.stdout.write(f"{img}")
        lastFrame = img.split("\n")
    else:
        # Check each line, and only update the parts that have changed
        # This is to reduce flickering and improve performance
        lines = img.split("\n")
        write = sys.stdout.write
        len_lastLines = len(lastFrame)
        len_lines = len(lines)
        for i in range(len_lines):
            # Check if the line has changed and only update those parts
            if i < len_lastLines and lines[i] != lastFrame[i]:
                write("\033[" + str(i+2) + ";0H")
                write(lines[i])
            else:
                # The scale has probably been changed
                write("\033[2;0H")
                write(f"{img}")
                break
        lastFrame = lines
            
    
    
    lastFrame = img
    writeTimeEnd = time.time()
    
    # Print the times
    extraInfo += (f"| Convert time: {format(round(convertTimeEnd - convertTimeStart, 4), '.4f')}s | Write time: {format(round(writeTimeEnd - writeTimeStart, 4), '.4f')}s ")

    while len(extraInfo)-8 < width+2: 
        extraInfo += "─"
    
    if "─" in extraInfo:
        extraInfo += "┐"

    sys.stdout.write("\033[0;0H")
    sys.stdout.write(extraInfo + "\n")

    # Skip frames to make sure we are playing at the correct fps
    # Calculate the frame we should be at
    frameWeShouldBeAt = round((time.time() - startTime + offset) * fps)
    # Calculate the difference between the frame we should be at and the frame we are at
    difference = frameWeShouldBeAt - frameNumber
    # If the difference is greater than 0, then we need to skip frames
    while difference > 0:
        # Increment the frame number
        frameNumber += 1
        # Decrement the difference
        difference -= 1
        # Increment the skipped frames
        skippedFrames += 1
    while difference < 0:
        # Increment the frame number
        frameNumber -= 1
        # Decrement the difference
        difference += 1


    # Calculate the fps
    if time.time() - lastSecondTime > 0.2:
        lastSecondFPSs.append(framesLastSecond * 5)
        lastSecondFPSs.pop(0)
        framesLastSecond = 0
        lastSecondTime = time.time()
        Fps = sum(lastSecondFPSs) / len(lastSecondFPSs)
    else:
        framesLastSecond += 1
    # If the difference is less than 0, then we need to wait
    if difference < 0:
        time.sleep(-difference/fps)

    cv2.waitKey(1)
