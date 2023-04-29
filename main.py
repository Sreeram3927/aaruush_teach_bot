import numpy as np
import time
import cv2
from pygame import mixer


Verbose = False

mixer.init()
drum_clap = mixer.Sound('batterrm.wav')
drum_snare = mixer.Sound('button-2.ogg')

blueLower = (80, 150, 10)
blueUpper = (120, 255, 255)

camera = cv2.VideoCapture(0)
ret, frame = camera.read()
H, W = frame.shape[:2]

kernal = np.ones((7, 7), np.uint8)

Hatt = cv2.resize(cv2.imread('./images/Hatt.png'), (200, 100), interpolation = cv2.INTER_CUBIC)
Snare = cv2.resize(cv2.imread('./images/Snare.png'), (200, 100), interpolation = cv2.INTER_CUBIC)

Hatt_centre = [np.shape(frame)[1]*2//8, np.shape(frame)[0]*6//8]
Snare_centre = [np.shape(frame)[1]*6//8, np.shape(frame)[0]*6//8]

Hatt_thickness = [200, 100]
Hatt_top = [Hatt_centre[0]-Hatt_thickness[0]//2, Hatt_centre[1]-Hatt_thickness[1]//2]
Hatt_btm = [Hatt_centre[0]+Hatt_thickness[0]//2, Hatt_centre[1]+Hatt_thickness]

Snare_thickness = [200, 100]
Snare_top = [Snare_centre[0]-Snare_thickness[0]//2, Snare_centre[1]-Snare_thickness[1]//2]
Snare_btm = [Snare_centre[0]+Snare_thickness[0]//2, Snare_centre[1]+Snare_thickness[1]//2]

time.sleep(1)


while True:

    ret, frame = camera.read()
    frame = cv2.flip(frame, 1)

    if not(ret):
        break

    snare_ROI = np.copy(frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]])
    mask = ROI_analsis(snare_ROI, 1)

    hatt_ROI = np.copy(frame[frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[1]]])
    mask = ROI_analysis(hatt_ROI, 2)

    cv2.putText(frame, 'Project: Air Drums (SD - beta)', (10, 30), 2, 1, (20, 20, 20), 2)

    if Verbose:

        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.bitwise_and(
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0], Snare_btm[0]],
            frame[Snare_top[1]:Snare_btm[1], Snare_top[0], Snare_btm[0]],
            mask = mask[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]]
        )

        frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]] = cv2.bitwise_and(
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0], Hatt_btm[0]],
            frame[Hatt_top[1]:Hatt_btm[1], Hatt_top[0], Hatt_btm[0]],
            mask = mask[Hatt_top[1]:Hatt_btm[1], Hatt_top[0]:Hatt_btm[0]]
        )

    else:

        frame[Snare_top[1]:Snare_btm[1], Snare_top[0]:Snare_btm[0]] = cv2.addWeighted(Snare, 1, frame[Snare_top[0]:Snare_btm[1], Snare_top[0]:Snare_btm[0]], 1, 0)