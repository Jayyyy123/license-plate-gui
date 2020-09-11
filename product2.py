import os

import cv2
import mysql.connector
import pyperclip

import char_detection
import plate_detection

SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False


def start():
    def sign_up_database():
        conn = mysql.connector.connect(host='localhost', user='root', port=3306, password='tanyijie1997',
                                       db='register', auth_plugin='mysql_native_password')
        c1 = conn.cursor()
        license_plate = main()
        c1.execute('SELECT * FROM sps_data where vehicle_plate_number=%s', (license_plate,))
        r = c1.fetchone()
        if r is not None:
            with open('./txt/knn_vehicle_details.txt', 'w') as f:
                print("Details:", file=f)
                print("ID : " + r[0], file=f)
                print("F_NO : " + r[1], file=f)
                # print("Employee ID : " + r[2], file=f)
                # print("Employee Name : " + r[3], file=f)
                print("Department : " + r[4], file=f)
                # print("Role : " + r[6], file=f)
                # print("Shift pattern : " + r[6], file=f)
                # print("Mobile Number : " + r[7], file=f)
                # print("Request date : " + r[8], file=f)
                # print("Request type : " + r[9], file=f)
                print("Vehicle type : " + r[10], file=f)
                print("Vehicle model : " + r[11], file=f)
                print("Vehicle plate number : " + r[12], file=f)
                print("Vehicle color : " + r[16], file=f)
                print("======================================", file=f)
                print("Authorized vehicle", file=f)

        else:
            with open('./txt/knn_vehicle_details.txt', 'w') as f:
                print("Unauthorized vehicle", file=f)

    def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
        ptCenterOfTextAreaX = 0
        ptCenterOfTextAreaY = 0
        ptLowerLeftTextOriginX = 0
        ptLowerLeftTextOriginY = 0
        sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
        plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape
        intFontFace = cv2.FONT_HERSHEY_SIMPLEX
        fltFontScale = float(plateHeight) / 30.0
        intFontThickness = int(round(fltFontScale * 1.5))
        textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)
        ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
         fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene
        intPlateCenterX = int(intPlateCenterX)
        intPlateCenterY = int(intPlateCenterY)
        ptCenterOfTextAreaX = int(intPlateCenterX)
        if intPlateCenterY < (sceneHeight * 0.75):
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))
        else:
            ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))
        textSizeWidth, textSizeHeight = textSize
        ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
        ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))
        cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace,
                    fltFontScale, SCALAR_YELLOW, intFontThickness)

    def main():
        blnKNNTrainingSuccessful = char_detection.loadKNNDataAndTrainKNN()
        if not blnKNNTrainingSuccessful:
            print("\nerror: KNN traning was not successful\n")
            return
        imgOriginalScene = cv2.imread(pyperclip.paste())
        if imgOriginalScene is None:
            print("\n1\n\n")
            os.system("pause")
            return
        listOfPossiblePlates = plate_detection.detectPlatesInScene(imgOriginalScene)
        listOfPossiblePlates = char_detection.detectCharsInPlates(listOfPossiblePlates)

        if len(listOfPossiblePlates) == 0:
            print("\nno license plates were detected\n")
        else:
            listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
            licPlate = listOfPossiblePlates[0]

            if len(licPlate.strChars) == 0:
                print("\nno characters were detected\n\n")
                return
            drawRedRectangleAroundPlate(imgOriginalScene, licPlate)
            with open('./txt/knn_vehicle_plate_number.txt', 'w') as f:
                print(licPlate.strChars, file=f)
            writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)
            imgOriginalSceneResize = cv2.resize(imgOriginalScene, (694, 371))

            cv2.imwrite("imgPlate.png", licPlate.imgPlate)
            cv2.imwrite("imgOriginalScene.png", imgOriginalSceneResize)
        cv2.waitKey(1000)
        return licPlate.strChars

    def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
        p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
        cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)

    sign_up_database()
