import time
from twilio.rest import Client
# Create a Twilio client

account_sid = 'AC8ae260fe96b882304daa131bb45dcd07'
auth_token = '24259bbc929fc2eef034a4d009b8d93e'

phone_number = 9907361281

phone_number = '+91' + str(phone_number)

client = Client(account_sid, auth_token)

message = client.messages.create(body='Dear {rec_name} \n We hope this message finds you well. '
                                          'We regret to inform you that your car({number})has been parked in violation of a no parking sign at {location}.'
                                          ' In order to avoid any inconvenience, we kindly request to pay a fine of ₹______ at (government created website). \n'
                                          ' Date and Time of Violation: {time} \n '
                                          'Please note that continued parking in this area may result in higher fines or towing.'
                                          ' We appreciate your prompt attention to this matter and cooperation in adhering to parking regulations. '
                                          '\n Thank you for understanding'.format(rec_name='(YOUR NAME)',number="(car_number)", location="(location)",time=time.ctime()),
                                     from_='+12532593038', to=phone_number)

print('Message sent to {number}'.format(number=phone_number))