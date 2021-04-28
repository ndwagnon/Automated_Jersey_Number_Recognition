#Author: Jeff Reidy and Noah Wagnon
#Description: Extracts game clock info from cropped
# raw footage


# Importing all necessary libraries 
import cv2
import numpy as np
import os
import pytesseract
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys

#Enforce that the user provides video path
if (len(sys.argv) < 2):
    print("Please provided video name as command-line-argument")
    exit()

#video path
videoPath = sys.argv[1]

#create the outfile. THis is 
outfile = open("ocr_raw_output.txt", 'w')

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Read the video from specified path 
cam = cv2.VideoCapture(videoPath) 
  
try: 
      
    # creating a folder named 'RawOCRFrames' 
    if not os.path.exists('RawOCRFrames'): 
        os.makedirs('RawOCRFrames') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 
    

# frame counters
processedframe = 0
currentframe = 0

while(True): 
      
    # reading from frame 
    ret,frame = cam.read() 
  
    if ret: 
        # if video is still left continue creating images 
        if (currentframe % 30) ==0:
            name = './RawOCRFrames/frame' + str(currentframe) + '.jpg'
#             print ('Creating...' + name) 
            
             
            # writing the extracted images 
            cv2.imwrite(name, frame)
            
            img1 = get_grayscale(frame)
            img2 = thresholding(img1)
            
            
#This is the frame crop the an SEC game
            crop_img = frame[610:655, 865:980]
            name2 = './RawOCRFrames/crop' + str(currentframe) + '.jpg'
#             print ('Creating...' + name2) 
            
            
            img1 = get_grayscale(crop_img)
            img2 = thresholding(img1)
            
            img2 = (255- img2)
            
            #dataPre stores raw result
            dataPre = pytesseract.image_to_string(img2)
            
            print(dataPre)
            #We will filter and format dataPost
            dataPost =""

            #Loop through and format
            for char in dataPre:
                if (char.isdigit() or char.isspace() ) and not(char == '\n'):
                    dataPost = dataPost + char

            #strip whitespace and ending character
            dataPost = dataPost[:-1]
            dataPost = dataPost.rstrip()
            dataPost = dataPost.lstrip()
            dataPost = dataPost.rstrip('\n')
            outfile.write(str(currentframe) + ' ')  
    
    # Attempting to implement code that writes (0 0 then makes a newline) if OCR detects nothing ie commercials, replays etc.) 
            if dataPost and (not dataPost.isspace()) and not (len(dataPost) < 3):

                #detect if play clock is missing and add 00
                if not (' ' in dataPost):
                    dataPost = dataPost + " 0"

                dataPost = dataPost + '\n'
                outfile.write(dataPost)
            else: 
                outfile.write("0 0\n")
            

            
            # Writes the cropped image to the same folder as the saved frames
            cv2.imwrite(name2, img2)
            processedframe = processedframe + 1

        
      
        
        
        
        # increasing counter so that it will 
        # show how many frames are created 
        currentframe += 1
        
    else: 
        break
        
outfile.close()
# # Release all space and windows once done 

cam.release() 
cv2.destroyAllWindows() 
