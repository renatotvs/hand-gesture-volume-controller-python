
import cv2
import numpy as np
import HandTrackingModule as htm
import math

#control volume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

############################################################
wCam, hCam = 640, 480
#wCam, hCam = 1200, 600
############################################################

camera = 0 #1

cap = cv2.VideoCapture(camera)

cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


#volume.GetMute()
#volume.GetMasterVolumeLevel()
print(volume.GetVolumeRange())

volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

vol = -20.0
volBar = 318 #360
volPerc = 20

while True:

    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        #print(lmList[2])
        #print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

        lengh = math.hypot(x2 - x1, y2 - y1)

        # Hand range 50 - 300
        # Volume Range -65 -0

        vol = np.interp(lengh, [50, 300], [minVol, maxVol])
        volBar = np.interp(lengh, [50, 300], [360, 150])
        volPerc = np.interp(lengh, [50, 300], [0, 100])

        print("volBar: ", volBar)

        print("volPerc: ", round(volPerc))

        #volume.SetMasterVolumeLevel(vol, None)
        volume.SetMasterVolumeLevelScalar(volPerc / 100, None)
        print(int(lengh), vol)

    else:
        # seta um volume padrão é o ultimo volume feito pelo movimento das mãos
        #volume.SetMasterVolumeLevel(vol, None)
        volume.SetMasterVolumeLevelScalar(volPerc / 100, None)

    cv2.rectangle(img, (50, 150), (85, 360), (255,0,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 360), (0, 255, 0), cv2.FILLED)

    cVol = round(volume.GetMasterVolumeLevelScalar() * 100) # mostra volume do windows
    cv2.putText(img, f'Vol: {cVol}', (40, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("img", img)

    k = cv2.waitKey(1) & 0xFF

    if k == 27 or k == 13:
        break
