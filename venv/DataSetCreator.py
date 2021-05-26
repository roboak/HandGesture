import cv2
import numpy as np
import json
import os
import io

class GestureMetaData:
    def __init__(self, gestureName):
        self.gestureName = gestureName
        self.trials = 0
        self.files = []

gestureMetaData = GestureMetaData("gesture1")
dataset = r"C:/Users/Akash/Documents/HandDataset"
PATH = dataset + "/" + "MetaData.json"


def UpdateMetaData(gestDict, videoFile):
    gestDict[gestureMetaData.gestureName]["trials"] += 1
    gestDict[gestureMetaData.gestureName]["files"].append(videoFile)
    with open(PATH, "w") as outfile:
        json.dump(gestDict, outfile)

def CreateDataSet():
    #Meta File Creation
    if not (os.path.isfile(PATH) and os.access(PATH, os.R_OK)):
        # JSON file already exist print ("File Present")
        with io.open(PATH, 'w') as db_file:
            db_file.write(json.dumps({}))
    file = open(PATH)
    gestDict = json.load(file)
    #print("MetaData: \n", gestDict)
    file.close()
    if not (gestureMetaData.gestureName in gestDict.keys()):
        gestDict[gestureMetaData.gestureName] = gestureMetaData.__dict__

    #Capturing Video
    cap = cv2.VideoCapture(0)
    #VideoName = gestureName_trialNo
    videoName = gestureMetaData.gestureName +'_'+ str(gestDict[gestureMetaData.gestureName]["trials"]+1) + '.avi'
    videoPath = dataset+'/'+ videoName
    UpdateMetaData(gestDict, videoName)
    print("Video Path: ", videoPath)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(videoPath, fourcc, 20.0, (640, 480))
    record = False
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        cv2.imshow("Gesture", image)
        k = cv2.waitKey(1)
        if(k%256 == 32):
            record = True
            print ("Set to Recording Mode")
        if(record):
            out.write(image)
            print("Recording")
        if k & 0xFF == ord('q'):
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


CreateDataSet()

