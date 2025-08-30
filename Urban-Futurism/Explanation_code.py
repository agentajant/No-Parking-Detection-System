import sys
import cv2
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
            First_Name_cell = worksheet.cell_value(x,1)
            Last_Name_cell = worksheet.cell_value(x,2)
            RTO_cell = worksheet.cell_value(x,3)
            Reg_date_cell = worksheet.cell_value(x,4)
            Eng_no_cell = worksheet.cell_value(x,5)

            print("This Car belongs to -")
            print("First Name: ", First_Name_cell)
            print("Last Name: ", Last_Name_cell)
            print("RTO Name: ",RTO_cell)
            print("Registeration Date: ", Reg_date_cell)
            print("Engine Number: ", Eng_no_cell)
            break


def scan_image(image_file):
    img = cv2.imread(image_file)

    cv2.imshow("WIN", img)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imshow("WIN", gray)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    bfilter = cv2.bilateralFilter(gray,11,17,17)

    cv2.imshow("WIN", bfilter)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    edged = cv2.Canny(bfilter, 30, 200)

    cv2.imshow("WIN", edged)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

    cropped_image = gray

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    result_text = result[len(result) - 1][-2]
    final_text = result_text.replace(" ", "")

    final_text = ''.join(letter for letter in final_text if letter.isalnum())

#    scan_data(final_text.upper())
    with open('number_plate.txt', 'w') as f:
        f.write(final_text.upper())


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