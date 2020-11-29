#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Import the relevant files
from sys import exit as Die
try:
    import cv2
    import numpy as np
    import math
    from colordetection import ColorDetector
except ImportError as err:
    Die(err)

'''
Testing variable
set to false to start task 2 & 3
'''
cameratesting = True 

'''
Initialize camera 
'''
cam_port         = 0
cam              = cv2.VideoCapture(cam_port)
i = 0


detector_stickers =[[300, 220], [400, 220],
                    [300, 320], [400, 320]]

current_stickers = [[20, 20], [54, 20],
                   [20, 54], [54, 54]]

recorded_stickers = [[20, 130], [54, 130],
                   [20, 164], [54, 164]]


def draw_detector_stickers(frame):
    for (x,y) in (detector_stickers):
        cv2.rectangle(frame, (x,y), (x+50, y+50), (255,255,255), 1)
    
        pass

def draw_current_stickers(frame, state):
    """Draws the 9 current stickers in the frame."""
    for index,(x,y) in enumerate(current_stickers):
        cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)
        #ColorDetector.name_to_rgb is generating an RGB value in format (R,G,B)
        #for white, you can use (255,255,255) as argument and (0,0,0) for black
        #-1 means the sticker is filled, 0 unfilled
    # your code here task 2.2

def draw_recorded_stickers(frame, state):
    """Draws the 9 preview stickers in the frame."""
    # for index,(x,y) in (recorded_stickers):
    for index,(x,y) in enumerate(recorded_stickers):
        cv2.rectangle(frame, (x,y), (x+32, y+32), ColorDetector.name_to_rgb(state[index]), -1)
    # your code here task 2.3

def color_to_notation(color):
    """
    Colors to notation
    """
    notation = {
        'green'  : 'F',
        'white'  : 'U',
        'blue'   : 'B',
        'red'    : 'R',
        'orange' : 'L',
        'yellow' : 'D'
    }
    return notation[color]

def numb_to_notation(i):
    notation = {
        1  : 'F',
        2  : 'U',
        3 : 'B',
        4 : 'R',
        5 : 'L',
        6 : 'D'
    }
    return notation[i]

def empty_callback(x):

    pass

def scan():


    sides   = {}                            # collection of scanned sides
    preview = ['white','white',     # default starting preview sticker colors
               'white','white',]
    state   = [0,0,                       # current sticker colors
               0,0]


    defaultcal = {                          # default color calibration
                'white':[[ 64, 173, 255],[3, 0, 0]],
                'green':[[104, 255, 255],[31, 85, 78]],
                'red':[[172, 255, 255], [7, 136, 148]],
                'orange':[[ 45, 255, 255], [ 17,  71, 186]],
                'yellow':[[ 48, 255, 242],[ 27, 178,  51]],
                'blue':[[172, 255, 255],[68,  0,  0]]
                }

    colorcal  = {}                          # color calibration dictionary
    color = ['white', 'green', 'red', 'orange', 'yellow', 'blue']  # list of valid colors            
    
    cv2.namedWindow('default',0)
    # create trackbars here   
    cv2.createTrackbar('H Upper','default',defaultcal[color[len(colorcal)]][0][0], 179, empty_callback)
    cv2.createTrackbar('S Upper','default',defaultcal[color[len(colorcal)]][0][1], 255, empty_callback)
    cv2.createTrackbar('V Upper','default',defaultcal[color[len(colorcal)]][0][2], 255, empty_callback)
    cv2.createTrackbar('H Lower','default',defaultcal[color[len(colorcal)]][1][0], 179, empty_callback)
    cv2.createTrackbar('S Lower','default',defaultcal[color[len(colorcal)]][1][1], 255, empty_callback)
    cv2.createTrackbar('V Lower','default',defaultcal[color[len(colorcal)]][1][2], 255, empty_callback)

  

    colorcal = defaultcal

    while cameratesting:
        global i
        _,frame = cam.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        key = cv2.waitKey(300)
        draw_detector_stickers(frame)
        # Bounds for HSV values we are interested in (Blue)
        # lower_hsv = np.array([89,178,51])     #hmin,smin,vmin
        # upper_hsv = np.array([118,255,194])   #hmax,smax,vmax
        # mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
        # frame = cv2.bitwise_and(frame,frame, mask= mask)
        
        # cv2.rectangle(frame, (200,200), (250, 250), (255,0,0), 2) 
        # # -1 borderwidth is a fill
        # cv2.rectangle(frame, (300,200), (350, 250), (0,0,255), -1)

        #preview a camera window
        # cv2.imshow('my_window_name', frame)	
        # value = cv2.getTrackbarPos('My track bar','my_window_name')
        
        # print(value)
     
       
        
        
        # init certain stickers.

        for index,(x,y) in enumerate(detector_stickers):
            # cv2.rectangle(frame, (x,y), (x+30, y+30), (255,255,255), 2)
            roi          = hsv[y:y+50, x:x+50]              # extracts hsv values within sticker
            avg_hsv      = ColorDetector.average_hsv(roi)    # filters the hsv values into one hsv
            color_name   = ColorDetector.get_color_name(avg_hsv,colorcal) # extracts the color based on hsv
            state[index] = color_name                       # stores the color 

            # update when space bar is pressed.

            if key == 32:
                i+=0.25
                preview = list(state)
                draw_recorded_stickers(frame, state)  # draw the saved colors on the preview
                face = numb_to_notation(math.ceil(i)) # convert the color to notation of the middle sticker and label this as the face
                # time.sleep(0.5)
                notation = [color_to_notation(color) for color in state] # convert all colors to notation
                sides[face] = notation              # update the face in the sides dictionary

        # show the new stickers
        draw_current_stickers(frame, state)                 # draw live sampling of face colors

        # append amount of scanned sides
        text = 'scanned sides: {}/6'.format(len(sides))
        cv2.putText(frame, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
        
       
        # quit on escape.
        if key == 27:
            break

        # show result
        cv2.imshow("default", frame)

    # show color calibration when pressing button c
        if key == 99:
            colorcal = {}   
            while len(colorcal) < 6:
                _, frame = cam.read()
                
                
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                key = cv2.waitKey(10) & 0xff

                # hue upper lower
                 # hue upper lower
                hu = cv2.getTrackbarPos('H Upper','default')
                hl = cv2.getTrackbarPos('H Lower','default')
                 # saturation upper lower
                su = cv2.getTrackbarPos('S Upper','default')
                sl = cv2.getTrackbarPos('S Lower','default')
                # value upper lower
                vu = cv2.getTrackbarPos('V Upper','default')
                vl = cv2.getTrackbarPos('V Lower','default')

                if color[len(colorcal)] == 'red' or color[len(colorcal)] == 'orange':
                    lower_hsv = np.array([0,sl,vl])
                    upper_hsv = np.array([hl,su,vu])
                    mask1 = cv2.inRange(hsv, lower_hsv, upper_hsv)
                    lower_hsv = np.array([hu,sl,vl])
                    upper_hsv = np.array([179,su,vu])
                    mask2 = cv2.inRange(hsv, lower_hsv, upper_hsv)
                    mask = cv2.bitwise_or(mask1, mask2)
                    res = cv2.bitwise_and(frame,frame, mask= mask)
                    lower_hsv = np.array([hl,sl,vl])
                    upper_hsv = np.array([hu,su,vu])
                else:
                    lower_hsv = np.array([hl,sl,vl])
                    upper_hsv = np.array([hu,su,vu])
                    
                    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
                    res = cv2.bitwise_and(frame,frame, mask = mask)
                
                if key == 32:
                    defaultcal[color[len(colorcal)]] = [upper_hsv,lower_hsv]
                    colorcal[color[len(colorcal)]] = [upper_hsv,lower_hsv]
                    print( [upper_hsv,lower_hsv]) 
                    
                    if(len(colorcal) < 6):
                        cv2.setTrackbarPos('H Upper','default',defaultcal[color[len(colorcal)]][0][0])
                        cv2.setTrackbarPos('S Upper','default',defaultcal[color[len(colorcal)]][0][1])
                        cv2.setTrackbarPos('V Upper','default',defaultcal[color[len(colorcal)]][0][2])
                        cv2.setTrackbarPos('H Lower','default',defaultcal[color[len(colorcal)]][1][0])
                        cv2.setTrackbarPos('S Lower','default',defaultcal[color[len(colorcal)]][1][1])
                        cv2.setTrackbarPos('V Lower','default',defaultcal[color[len(colorcal)]][1][2])

                if(len(colorcal) < 6):
                    text = 'calibrating {}'.format(color[len(colorcal)])
                cv2.putText(res, text, (20, 460), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)

                cv2.imshow("default", res)
                # quit on escape key.
                if key == 27:
                    break

    cam.release()
    cv2.destroyAllWindows()
    return sides if len(sides) == 6 else False


