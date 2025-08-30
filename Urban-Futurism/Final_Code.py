import sys
import cv2
import easyocr
import requests
from twilio.rest import Client
import time

key = '1533020cc6mshd7dfca12905cff6p1cc03ajsn26b9b8b9c9ab'
host = 'rto-vehicle-information-verification-india.p.rapidapi.com'

account_sid = 'AC8ae260fe96b882304daa131bb45dcd07'
auth_token = '24259bbc929fc2eef034a4d009b8d93e'

loc = 'SPSRN BHOPAL'

#PARAMETERS
my_number = '+917223098337'
number_plate = 'MP07ZC8090'
self_message = True
waiting = True
video = False
img_scanning = True

cap = cv2.VideoCapture(0)

def scan_image(image_file):
    img = cv2.imread(image_file)

    if waiting:
        cv2.imshow("WIN", img)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if waiting:
        cv2.imshow("WIN", gray)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    bfilter = cv2.bilateralFilter(gray,11,17,17)

    if waiting:
        cv2.imshow("WIN", bfilter)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    edged = cv2.Canny(bfilter, 30, 200)

    if waiting:
        cv2.imshow("WIN", edged)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

    cropped_image = gray

    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image)
    result_text = result[len(result) - 1][-2]
    final_text = result_text.replace(" ", "")

    final_text = ''.join(letter for letter in final_text if letter.isalnum())
    text = str(final_text.upper())

    a = text[0:2]    #Letter
    b = text[2:4]   #Number
    c = text[4:6]   #Letter
    d = text[6:10]  #Number

    part1 = a.replace('0', 'O')
    part1 = a.replace('1', 'L')

    part2 = b.replace('O', '0')
    part2 = b.replace('Y', '4')
    part2 = b.replace('L', '4')

    part3 = c.replace('0', 'O')
    part3 = c.replace('1', 'L')
    part4 = d.replace('O', '0')

    part4 = d.replace('Y', '4')
    part4 = d.replace('L', '4')

    text = part1 + part2 + part3 + part4
    end_text = ''.join(letter for letter in text if letter.isalnum())

    print(end_text)
 #   data_extractor(end_text)

def data_extractor(num_plate):
    url = "https://rto-vehicle-information-verification-india.p.rapidapi.com/api/v1/rc/vehicleinfo"

    payload = {
        "reg_no": num_plate,
        "consent": "Y",
        "consent_text": "I hear by declare my consent agreement for fetching my information via AITAN Labs API"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": key,
        "X-RapidAPI-Host": host
    }

    response = requests.post(url, json=payload, headers=headers)
    result = response.json()
    print(result)
    if result['result']['mobile_no'] == None:
        print("Number Not given")
        sys.exit()
    else:
        num = '+91' + (str(result['result']['mobile_no']))
        print('\n',num)
 #   SendSMS(str(result['result']['owner_name']), num_plate, num, loc)

def SendSMS(name, car_number, phone_number, location):
    client = Client(account_sid, auth_token)

    message = client.messages.create(body='Dear {rec_name} \n We hope this message finds you well. '
                                          'We regret to inform you that your car({number})has been parked in violation of a no parking sign at {location}.'
                                          ' In order to avoid any inconvenience, we kindly request to pay a fine of ₹______ at (government created website). \n'
                                          ' Date and Time of Violation: {time} \n '
                                          'Please note that continued parking in this area may result in higher fines or towing.'
                                          ' We appreciate your prompt attention to this matter and cooperation in adhering to parking regulations. '
                                          '\n Thank you for understanding'.format(rec_name=name,number=car_number, location=location,time=time.ctime()),
                                     from_='+12532593038', to=phone_number)

    if self_message:
        message = client.messages.create(body='Dear {rec_name} \n We hope this message finds you well. '
                                              'We regret to inform you that your car({number})has been parked in violation of a no parking sign at {location}.'
                                              ' In order to avoid any inconvenience, we kindly request to pay a fine of ₹______ at (government created website). \n'
                                              ' Date and Time of Violation: {time} \n '
                                              'Please note that continued parking in this area may result in higher fines or towing.'
                                              ' We appreciate your prompt attention to this matter and cooperation in adhering to parking regulations. '
                                              '\n Thank you for understanding'.format(rec_name=name, number=car_number,
                                                                                      location=location,
                                                                                      time=time.ctime()),
                                         from_='+12532593038', to=my_number)

    print('\n Message sent to {number}'.format(number=phone_number))
    sys.exit()

if video == False and img_scanning == True:
    scan_image('NUM_PLATE.jpg')
if video == False and img_scanning == False:
    data_extractor(number_plate)

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

#    print(response.json())