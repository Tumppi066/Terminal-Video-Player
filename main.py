if __name__ == "__main__":
    
    import cv2 # CV2 Is used to read the video file
    import time # Time is used to sync the frames correctly
    from convertToAscii import convertToAscii, convertToAsciiTraditional # Import the convertToAscii function
    import os # OS is used to clear the console
    import mainMenu as menu # Import the main menu
    import sys

    # Ask the user for the video file name, fps and width
    video, fps, width, style, show, useTraditional, color = menu.Information()

    # If the style is custom, parse the characters
    if ";" in style:
        onPixel = style.split(";")[0]
        offPixel = style.split(";")[1]
        style = "custom"

    # Clear the screen
    os.system("cls")

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

    while True:

        # Read the next video frame and increment the frame number
        success, img = video.read()
        frameNumber += 1

        
        # If the video is over, break the loop
        if(success == False): 
            os.system("cls")
            print("> Video file not found / video ended")
            break
        
        
        # Print the current time
        extraInfo = f"┌ Frame: {frameNumber}/{length} | {format(round(frameNumber/30, 2), '.2f')}s | "
        # - Frame number
        percentage = round(frameNumber/length*100, 2)
        extraInfo += f"{format(percentage, '.2f')}% | "
        # - Skipped frames
        extraInfo += f"\033[91m{skippedFrames} ({format(round(skippedFrames/frameNumber*100, 2), '.2f')}%) skipped frames\033[97m)"
        # - FPS
        extraInfo += f" | FPS: {format(round(Fps, 2), '.2f')} "
        # Print the controls
        extraInfo += f" | Use CTRL+C to exit "
        

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
        if style == "custom" and useTraditional == "y":
            img = convertToAsciiTraditional(img, width, onSymbol=onPixel, offSymbol=offPixel)
        elif useTraditional == "y":
            img = convertToAsciiTraditional(img, width, characterSet=style)
        elif color == "y":
            img = convertToAscii(img, percentage, width, color=True)
        else:
            img = convertToAscii(img, percentage, width)

        # - Rest of the box
        while len(extraInfo)-8 < width+2: 
            extraInfo += "─"
        
        if "─" in extraInfo:
            extraInfo += "┐"
        
        # Clear the console and print the current frame
        os.system('cls')
        sys.stdout.write(extraInfo + "\n")
        sys.stdout.write(img)

        # Skip frames to make sure we are playing at the correct fps
        # Calculate the frame we should be at
        frameWeShouldBeAt = round((time.time() - startTime) * fps)
        # Calculate the difference between the frame we should be at and the frame we are at
        difference = frameWeShouldBeAt - frameNumber
        # If the difference is greater than 0, then we need to skip frames
        while difference > 0:
            # Read the next frame
            success, img = video.read()
            # Increment the frame number
            frameNumber += 1
            # Decrement the difference
            difference -= 1
            # Increment the skipped frames
            skippedFrames += 1

        # Calculate the fps
        Fps = (frameNumber-skippedFrames) / (time.time() - startTime)
        # If the difference is less than 0, then we need to wait
        if difference < 0:
            time.sleep(-difference/fps)

        cv2.waitKey(1)

