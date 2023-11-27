
if __name__ == "__main__":
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
    from ffpyplayer.player import MediaPlayer
    import threading
    import shutil

    # Ask the user for the video file name, fps and width
    # videoPath, fps, width, style, show, useTraditional, color = menu.Information()
    
    # Get all videos in the current directory
    videos = [f for f in os.listdir('.') if os.path.isfile(f) and ".mp4" in f]
    selectedFile = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("Please select a video file")
        for i in range(len(videos)):
            if i == selectedFile:
                print(f"> {videos[i]}")
            else:
                print(f"  {videos[i]}")
        
        if keyboard.is_pressed("up"):
            selectedFile -= 1
        elif keyboard.is_pressed("down"):
            selectedFile += 1
        elif keyboard.is_pressed("enter"):
            break
        elif keyboard.is_pressed("esc"):
            exit()
        
        if selectedFile < 0:
            selectedFile = 0
        elif selectedFile > len(videos)-1:
            selectedFile = len(videos)-1
            
        time.sleep(0.05)
        
    time.sleep(0.2)
    videoPath = videos[selectedFile]
    
    # Read the video fps and width
    video = cv2.VideoCapture(videoPath)
    fps = video.get(cv2.CAP_PROP_FPS)
    videoWidth, videoHeight = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video.release()

    # Check what width the video can run at 
    terminal_size = shutil.get_terminal_size(fallback=(120, 50))
    termWidth = terminal_size.columns
    termHeight = terminal_size.lines
    newWidth = videoWidth
    newHeight = videoHeight
    # Now lower the width until it fits in the terminal
    while True:
        if newWidth > termWidth or newHeight > termHeight:
            newWidth -= 1
            newHeight = int(newWidth/videoWidth*videoHeight)
        else:
            break
    
    width = newWidth
    
    # Ask the user if they want to use color
    colorChoices = ["Yes", "No"]
    colorChoice = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("Do you want to use color?")
        for i in range(len(colorChoices)):
            if i == colorChoice:
                print(f"> {colorChoices[i]}")
            else:
                print(f"  {colorChoices[i]}")
        
        if keyboard.is_pressed("up"):
            colorChoice -= 1
        elif keyboard.is_pressed("down"):
            colorChoice += 1
        elif keyboard.is_pressed("enter"):
            break
        elif keyboard.is_pressed("esc"):
            exit()
        
        if colorChoice < 0:
            colorChoice = 0
        elif colorChoice > len(colorChoices)-1:
            colorChoice = len(colorChoices)-1
    
        time.sleep(0.05)
    
    time.sleep(0.2)
    color = colorChoices[colorChoice]
    color = True if color == "Yes" else False
    
    # Ask the user if they want to use traditional ascii characters
    useTraditionalChoices = ["No", "Yes"]
    useTraditionalChoice = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("Do you want to use traditional ascii characters?")
        for i in range(len(useTraditionalChoices)):
            if i == useTraditionalChoice:
                print(f"> {useTraditionalChoices[i]}")
            else:
                print(f"  {useTraditionalChoices[i]}")

        if keyboard.is_pressed("up"):
            useTraditionalChoice -= 1
        elif keyboard.is_pressed("down"):
            useTraditionalChoice += 1
        elif keyboard.is_pressed("enter"):
            break
        elif keyboard.is_pressed("esc"):
            exit()
        
        if useTraditionalChoice < 0:
            useTraditionalChoice = 0
        elif useTraditionalChoice > len(useTraditionalChoices)-1:
            useTraditionalChoice = len(useTraditionalChoices)-1

        time.sleep(0.05)
            
    time.sleep(0.2)
    useTraditional = useTraditionalChoices[useTraditionalChoice]
    useTraditional = True if useTraditional == "Yes" else False

    def parse_subtitles(filename):
        with open(filename, 'r', encoding="utf-8") as f:
            lines = f.readlines()

        subtitles = []
        i = 0
        while i < len(lines):
            # Skip non-subtitle lines
            if '-->' not in lines[i]:
                i += 1
                continue

            # Parse the start and end times
            times = lines[i].strip().split(' --> ')
            start_time = sum(float(x) * 60 ** (2 - j) for j, x in enumerate(times[0].replace(',', '.').split(':')))
            end_time = sum(float(x) * 60 ** (2 - j) for j, x in enumerate(times[1].replace(',', '.').split(':')))

            # Parse the subtitle
            subtitle = lines[i + 1].strip()

            # Add the subtitle to the list
            subtitles.append((subtitle, (start_time, end_time)))

            i += 2

        return subtitles

    # Check if a subtitle file exists
    # subtitlePath = videoPath.split(".")[0] + ".srt"
    # if os.path.isfile(subtitlePath):
    #     # Read the subtitles and store them in a dictionary with their start and end times
    #     subtitleDict = parse_subtitles(subtitlePath)
    #     for subtitle, times in subtitleDict:
    #         print(f"Added subtitle: {subtitle} ({times[0]} - {times[1]}))")

    try:
        sortedSubtitles = sorted(subtitleDict, key=lambda x: x[1][0])
    except:
        sortedSubtitles = None
    
    # Read the video
    video = cv2.VideoCapture(videoPath)
    player = MediaPlayer(videoPath, ff_opts={'volume':0.1})
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

    lastFps = 0
    changedSize = 0
    
    currentSubtitle = None
    fpsStartTime = time.time()
    fpsEndTime = 1
    
    audioStartTime = 1
    audioEndTime = 2

    dontLoadNextFrame = 0
    lastimg = None

    
    lastTerminalSize = shutil.get_terminal_size(fallback=(120, 50))
    while True:
        lastFpsStartTime = fpsStartTime
        fpsStartTime = time.time()
        fastForwarded = False

        # Detect left and right keypresses to skip / revind 5s of the video
        if keyboard.is_pressed("left") and inputTimer + inputPadding < time.time():
            offset -= 2 / (30/fps)
            fastForwarded = True


        if keyboard.is_pressed("right") and inputTimer + inputPadding < time.time():
            offset += 2 / (30/fps)
            fastForwarded = True
        
        # Autodetect terminal size and set the width to that
        if keyboard.is_pressed("a") and inputTimer + inputPadding < time.time() or shutil.get_terminal_size() != lastTerminalSize:
            # Do the same calculation as above at startup
            termWidth = shutil.get_terminal_size().columns
            termHeight = shutil.get_terminal_size().lines
            newWidth = videoWidth
            newHeight = videoHeight
            # Now lower the width until it fits in the terminal
            while True:
                if newWidth > termWidth or newHeight > termHeight:
                    newWidth -= 1
                    newHeight = int(newWidth/videoWidth*videoHeight)
                else:
                    break
            
            print(f"Terminal size: {termWidth}x{termHeight}")
            print(f"Autodetected size: {newWidth}x{newHeight} ({round((newWidth/videoWidth)*100, 1)}x{round((newHeight/videoHeight)*100, 1)}%)")
            input()
            width = newWidth
            changedSize = 2
            inputTimer = time.time()
            os.system("cls" if os.name == "nt" else "clear")
            lastTerminalSize = shutil.get_terminal_size()

        # Detect the up and down keypresses to increase / decrease the width
        if keyboard.is_pressed("up") and inputTimer + inputPadding < time.time():
            width += 5
            changedSize = 2
            inputTimer = time.time()
            os.system("cls" if os.name == "nt" else "clear")
            lastTerminalSize = shutil.get_terminal_size()
            
        if keyboard.is_pressed("down") and inputTimer + inputPadding < time.time():
            width -= 5
            changedSize = 2
            inputTimer = time.time()
            os.system("cls" if os.name == "nt" else "clear")
            lastTerminalSize = shutil.get_terminal_size()
            
        # Detect the space keypress to pause / play the video
        if keyboard.is_pressed("space") and inputTimer + inputPadding < time.time():
            paused = not paused
            inputTimer = time.time()
            print("Paused" if paused else "Playing")
            
        # If we press esc quit
        if keyboard.is_pressed("esc") and inputTimer + inputPadding < time.time():
            break
            
        # Use r to reset back to frame 1 (and pause the video)
        if keyboard.is_pressed("r") and inputTimer + inputPadding < time.time():
            frameNumber = 1
            offset = 0
            paused = True
            
        if paused:
            # Lower the offset to compensate for the time we are paused
            if startPause == 0:
                startPause = time.time()
                player.set_pause(True)
            continue    
        else:
            if startPause != 0:
                endPause = time.time()
                offset -= endPause - startPause
                startPause = 0
                endPause = 0
                player.set_pause(False)

        # Read the next video frame and increment the frame number
        if dontLoadNextFrame > 0:
            dontLoadNextFrame -= 1
            img = lastimg
        else:
            success, img = video.read()
            lastimg = img
            frameNumber += 1

        frameNumber = video.get(cv2.CAP_PROP_POS_FRAMES)
        
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
        # Print the controls
        extraInfo += f" | Use ESC to exit (arrow keys for control) "
        # Merge extra info with
        # the box characters
        
        # Add the FPS to the video 
        if lastFps > fps:
            # Scale it with the video width
            videoWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            # Default is 480p so scale based on that
            aspect = videoWidth/480
            img = cv2.putText(img, f"{int(fps)}", (0, int(30*aspect)), cv2.FONT_HERSHEY_SIMPLEX, aspect, (0, 255, 0), int(2*aspect))
        else:
            # Scale it with the video width
            videoWidth = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            # Default is 480p so scale based on that
            aspect = videoWidth/480
            # Smoothly lerp between red (1/2fps) and green (fps)
            R = (0,0,255)
            G = (0,255,0)
            fpsColor = (int(R[0] + (G[0]-R[0]) * (lastFps/fps)), int(R[1] + (G[1]-R[1]) * (lastFps/fps)), int(R[2] + (G[2]-R[2]) * (lastFps/fps)))
            img = cv2.putText(img, f"{int(lastFps)}", (0, int(30*aspect)), cv2.FONT_HERSHEY_SIMPLEX, aspect, fpsColor, int(2*aspect))

        # Add the video dimensions to the video
        if changedSize > 0:
            videoWidth, videoHeight = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
            aspect = videoHeight/videoWidth
            newHeight = int(width/aspect/2)
            newWidth = int(width)
            img = cv2.putText(img, f"{newWidth}x{newHeight} ({round((newWidth/videoWidth)*100, 1)}x{round((newHeight/videoHeight)*100, 1)}%)", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 100, 255), 2)
            # Reduce the changedSize variable according to the framerate
            changedSize -= 1/fps


        # If `currentSubtitle` is `None` or the current time is not within the start and end times of `currentSubtitle`
        if sortedSubtitles is not None:
            currentTime = frameNumber / fps
            if currentSubtitle is None or not (float(currentSubtitle[1][0]) <= currentTime <= float(currentSubtitle[1][1])):
                # Find the next subtitle whose start time is less than or equal to the current time and whose end time is greater than the current time
                for subtitle, times in sortedSubtitles:
                    if float(times[0]) <= currentTime <= float(times[1]):
                        currentSubtitle = (subtitle, times)
                        break

            # If `currentSubtitle` is not `None`, display it on the video
            if currentSubtitle is not None:
                img = cv2.putText(img, currentSubtitle[0], (0, int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))-30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 100, 255), 2, cv2.LINE_AA)

        # Convert to B&W
        if not color:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
        
        # Convert the current video frame to ASCII
        convertTimeStart = time.time()
        if color:
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
            
            write = sys.stdout.write
            # Check each line, and only update the parts that have changed
            # This is to reduce flickering and improve performance
            lines = img.split("\n")
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
        extraInfo += (f"| Convert time: {format(round(convertTimeEnd - convertTimeStart, 4), '.4f')}s | Write time: {format(round(writeTimeEnd - writeTimeStart, 4), '.4f')}s | Audio time: {format(round(audioEndTime - audioStartTime, 4), '.4f')}s ")
        # Print the immediate fps
        try:
            extraInfo += f"| Current FPS: {str(round(1/(fpsEndTime-lastFpsStartTime),1))} "
            lastFps = round(1/(fpsEndTime-lastFpsStartTime),1)
        except:
            pass
        
        
        while len(extraInfo)-8 < width+2: 
            extraInfo += "─"
        
        if "─" in extraInfo:
            extraInfo += "┐"

        sys.stdout.write("\033[0;0H")
        sys.stdout.write(extraInfo + "\n")

        audioStartTime = time.time()
        audio_frame, val = player.get_frame(force_refresh=True, show=True)
        
        if val != 'eof' and audio_frame is not None:
            #audio
            ffpyplayerImage, t = audio_frame

        try:
            img, t = audio_frame
        except:
            continue
        
        # Calculate the frame we should be at based on the current audio time
        frameWeShouldBeAt = round((t+offset) * fps)
        difference = frameWeShouldBeAt - frameNumber
        
        # Seek the audio player to the correct frame (it takes input as seconds so we need to convert it)
        if fastForwarded:
            secondWeShouldBeAt = round((t + offset))
            player.seek(secondWeShouldBeAt, relative=False, accurate=True) 
            offset = 0
            fastForwarded = False
            # Seek the video to the correct frame
            video.set(cv2.CAP_PROP_POS_FRAMES, frameWeShouldBeAt)
        
        # If the difference is greater than 0, then we need to skip frames
        while difference > 0:
            # Increment the frame number
            frameNumber += 1
            # Decrement the difference
            difference -= 1
            # Increment the skipped frames
            if not fastForwarded:
                skippedFrames += 1
            # Read the next video frame
            success, img = video.read()
            # If the video is over, break the loop
            if(success == False): 
                os.system("cls" if os.name == "nt" else "clear")
                print("> Video file not found / video ended")
                break
            
        if difference < 0:
            # Decrement the frame number
            frameNumber -= 1
            # Decrement the difference
            difference += 1
            # Don't load the next frame to slow down the video
            dontLoadNextFrame += 1
            
        
        audioEndTime = time.time()
        fpsEndTime = time.time()
