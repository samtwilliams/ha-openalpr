#
# 15/09/2019 Commented out cv2 and imshow
#
#

import numpy as np
import cv2
import sys
from openalpr import Alpr
import requests
import datetime
from envs import env

HA_ENDPOINT = env('HA_APIENDPOINT') #'http://192.168.1.68:8123/api/services/script/turn_on'
HA_APIPASS = env('HA_APIPASSWORD')
PLATES = ['GU18GWV', 'RL19FJF','OY18GVK','MD67HTV', 'DC17DFP', 'LN66YNF', 'MF65UGS']
RTSP_SOURCE  = env('STREAM_SOURCE') #'rtsp://192.168.0.60/mpeg4'
WINDOW_NAME  = 'openalpr'
FRAME_SKIP   = 10


def open_cam_rtsp(uri):
    return cv2.VideoCapture(uri)

def main():
    alpr = Alpr('gb', '/srv/openalpr/openalpr.conf', '/srv/openalpr/runtime_data')
    if not alpr.is_loaded():
        print('Error loading OpenALPR')
        sys.exit(1)
    alpr.set_top_n(3)
    #alpr.set_default_region('new')

    cap = open_cam_rtsp(RTSP_SOURCE)
    if not cap.isOpened():
        alpr.unload()
        sys.exit('Failed to open video file!')
    #cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
    #cv2.setWindowTitle(WINDOW_NAME, 'OpenALPR video test')

    _frame_number = 0
    #declare a stamp 10 minutes ago, initialise variable when script starts
    STAMP = datetime.datetime.now() - datetime.timedelta(minutes=10)
    while True:
        ret_val, frame = cap.read()
        if not ret_val:
            print(datetime.datetime.now())
            print('VidepCapture.read() failed. Exiting...')
            break

        _frame_number += 1
        if _frame_number % FRAME_SKIP != 0:
            continue
        #cv2.imshow(WINDOW_NAME, frame)
        ret, enc = cv2.imencode("*.jpg", frame)
        results = alpr.recognize_array(enc.tobytes())

        #results = alpr.recognize_ndarray(frame)
        for i, plate in enumerate(results['results']):
            best_candidate = plate['candidates'][0]
            print(datetime.datetime.now() + ' Plate #{}: {:7s} ({:.2f}%)'.format(i, best_candidate['plate'].upper(), best_candidate['confidence']))
            
            #Does the plate match known plates
            if best_candidate['plate'].upper() in PLATES:

                #Has the gate fired recently? If not in the last 10 minutes then allow to fire again
                if datetime.datetime.now() > STAMP:
                    print("Recognised")
                    #If a plate is recongised set a timestamp to prevent it firing lots of times until time has expired
                    print(datetime.datetime.now())

                    #Open the gate
                    response = requests.post(
                        HA_ENDPOINT,
                        headers={'Content-Type': 'application/json', 'x-ha-access': '' + HA_APIPASS + '' },
                        data='{"entity_id": "script.ANPR"}',
                    )
                    STAMP = STAMP = datetime.datetime.now() + datetime.timedelta(minutes=3)
                else:
                    print("Not firing as time has not exceeded")

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()
    cap.release()
    alpr.unload()


if __name__ == "__main__":
    main()