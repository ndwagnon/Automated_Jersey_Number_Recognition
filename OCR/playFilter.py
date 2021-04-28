#Author: Noah Wagnon and Jeff Reidy
#Description: Uses process ocr frames
# to extract play windows


#create the outfile and read infile
outfile = open("ocr_filtered_output.txt", 'w')
infile = open("ocr_raw_output.txt", 'r')

#variables to keep up with clock values
gameClockCurrent = 1500
gameClockPrev = 1500
gameClockStart = 1500
snapClockPrev = 40
snapClock = 40
quarter = 1
playNumber = 1
framePrev = 0
startFrame = 0
endFrame = 0

#loop through each line
for line in infile:

    #extract each string
    values = line.split()
    
    if len(values) < 3:
        continue

    #convert to meaningful variables for current readings
    absFrame = int(values[0])

    
    if (int(values[1]) <= 1500):
        #ensure between 0-60 for second value

        if (int(values[1]) % 100 <= 59):
            gameClockReading = int(values[1])
        
        if (gameClockReading > gameClockPrev) and (gameClockPrev > 100):
            gameClockReading = gameClockPrev
    if int(values[2]) <= 40:
        snapClockReading = int(values[2])
    # print("absFrame: " + str(absFrame))
    # print("gameClockReading: " + str(gameClockReading))
    # print("snapClockReading: " + str(snapClockReading))

    #update the quarter
    if(gameClockReading > (gameClockCurrent + 1000) and not(gameClockReading == 0)):
        quarter = quarter + 1
        gameClockCurrent = 1500

    #update the gameclock
    if not(gameClockReading == 0) and not(gameClockReading > 1500):
        #edge case: make sure we are seeing full OCR and not skipping too much
        if abs(gameClockCurrent-gameClockReading) > 50:
            if gameClockReading > gameClockCurrent:
                continue
        
        if abs(gameClockCurrent - gameClockReading) > 200:
            continue
        
      
        gameClockCurrent = gameClockReading
        

    #update the playclock
    if not(snapClockReading == 0) and not(snapClockReading > 40):
        snapClockPrev = snapClock
        snapClock = snapClockReading
    
    snapDiff = snapClock-snapClockPrev
    #register a new play
    if ( (not(snapClockReading == 0) and (snapDiff > 5) ) and not(gameClockCurrent == gameClockPrev) ) or (abs(gameClockCurrent - gameClockPrev) > 40):
        endFrame = values[0]
        if (snapClock < snapClockPrev):
            gameClockPrev = gameClockCurrent
        #print format to include strings
        #outfile.write("Play number: " + str(playNumber) + " Quarter: " + str(quarter) + " Start frame: "  + str(startFrame) +
         #" End frame: " + str(framePrev) + " Start play time: " + str(gameClockStart) + " End play time: " + str(gameClockPrev) + '\n')

        #remove all info but numbers
        outfile.write(str(playNumber) + " " + str(quarter) + " "  + str(startFrame) +
         " " + str(framePrev) + " " + str(gameClockStart) + "  " + str(gameClockPrev) + '\n')

        startFrame = absFrame
        gameClockStart = gameClockCurrent
        playNumber = playNumber + 1
    
    #update gameClockPrev
    gameClockPrev = gameClockCurrent
    framePrev = absFrame

outfile.close()
