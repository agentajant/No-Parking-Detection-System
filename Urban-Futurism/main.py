import sys
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import xlrd

video = True

cap = cv2.VideoCapture(0)

def scan_data(text):
    print(text)
    workbook = xlrd.open_workbook('Registeration_data.xls')
    worksheet = workbook.sheet_by_index(0)
    for x in range(2,5):
        active_cell = worksheet.cell_value(x, 0)
        if str(active_cell).upper() == text:
            Name_cell = worksheet.cell_value(x,1)
            print('This Car Belongs to ' + str(Name_cell))
            break


def scan_image(image_file):
    img = cv2.imread(image_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bfilter = cv2.bilateralFilter(gray,11,17,17)
    edged = cv2.Canny(bfilter, 100, 200)

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10 ,True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x,y) = np.where(mask==255)
    (x1,y1) = (np.min(x), np.min(y))
    (x2,y2) = (np.max(x), np.max(y))
    cropped_image = gray[x1:x2+1, y1:y2+1]

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    result_text = result[len(result) - 1][-2]
    final_text = result_text.replace(" ", "")

    scan_data(final_text.upper())


if video == False:
    scan_image('DATA/Plate1.png')


while video:
    ret, frame = cap.read()

    cv2.imshow('Input', frame)

    c = cv2.waitKey(1)
    if c == 27:
        break
    if c == ord('b'):
        cv2.imwrite('cam.png',frame)
        scan_image('cam.png')
cap.release()
cv2.destroyAllWindows()

