# Author: Alex Ramey
# Modified by Noah Wagnon
# main.py accepts the path to a video clip of college football broadcast footage
# and plays it back with player numbers boxed.


from cv2 import cv2
from detector import Detector
import numpy as np
from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
import os
import sys
import threading
import time
import json

# Shared Thread Memory
plainFrame, labelledFrame = None, None

#global frame counter
frameCount = 0

def playVideo(video, lock):
    global plainFrame, labelledFrame, frameCount
    time.sleep(40)
  
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)

    while(cap.isOpened()):
        ret, frame = cap.read()
        frameCount += 1
        cv2.imshow('framereal', frame)
        #time.sleep(0.03333)
        if frame is None:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        with lock:
            if (plainFrame is None) and (labelledFrame is None):
                plainFrame = frame.copy() # start-up condition
            elif (plainFrame is None) and (labelledFrame is not None):
                labelledFrame = cv2.cvtColor(labelledFrame, cv2.COLOR_RGB2BGR)
                cv2.imshow('frame', labelledFrame)
                plainFrame = frame.copy()
                labelledFrame = None
        key = cv2.waitKey(int(1000/fps + .5))
        if key & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def detector(lock, isCrimson, debug=False):
    global plainFrame, labelledFrame, frameCount
    d = Detector(isCrimson,debug=debug)
    debugCount = 0
    #time.sleep(5)
    while(True):
        time.sleep(.01) # ~100 Hz
        frame = None
        with lock:
            if (plainFrame is not None) and (labelledFrame is None):
                frame = plainFrame       
                #cv2.imshow('frame', frame)
        if frame is None:
            continue
        
        # run detector on the frame
        print("Beginning Frame")
        results = d.detect(frame, frameCount)
        frame = Image.fromarray(frame)
        annotateFrame(frame, results)
        print("Frame Processed")
        if debug:
            debugCount += 1
            frame.save(os.path.join('debug/frames', 'frame_' + str(debugCount) + '_labelled.jpg'))
        with lock:
            plainFrame = None
            labelledFrame = np.array(frame)

def annotateFrame(frame, results):
    colors = list(ImageColor.colormap.values())
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(frame)

    boxes = results['rois']
    for i, box in enumerate(boxes):
        top = box[0]
        bottom = box[2]
        left = box[1]
        right = box[3]
        class_name = results['class_names'][i]
        label = "{}: {}%".format(class_name, int(results['scores'][i] * 100))
        color = colors[int(class_name) % len(colors)]
        segments = [(left, top), (left, bottom), (right, bottom), (right, top), (left, top)]
        draw.line(segments, width=4, fill=color)
        label_width, label_height = font.getsize(label)
        margin = np.ceil(0.05 * label_height)
        if top > (label_height + 2 * margin): # 0.05% margin
            label_bottom = top
        else:
            label_bottom = bottom + label_height + 2 * margin
        draw.rectangle([(left, label_bottom - label_height - 2 * margin), (left + label_width, label_bottom)], fill=color)
        draw.text((left + margin, label_bottom - label_height - margin), label, fill="black", font=font)

def main():
    if ((len(sys.argv) < 2) or (not os.path.exists(sys.argv[1]))):
        sys.exit("Please provide the input video file as a cmd line argument")

    #CLA for color   
    isCrimson = True #default to crimson

    if (len(sys.argv) == 3):
        color = sys.argv[2]
        if (color == 'white'):
            isCrimson = False
            
    lock = threading.Lock()
    debug = True
    #debug = False

    threading.Thread(target=detector, args=(lock, isCrimson, debug), daemon=True).start()

    playVideo(sys.argv[1], lock)

if __name__ == '__main__':
    main()
