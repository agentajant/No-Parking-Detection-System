import requests

url = "https://rto-vehicle-information-verification-india.p.rapidapi.com/api/v1/rc/vehicleinfo"

payload = {
	"reg_no": "MP04CX4011",
	"consent": "Y",
	"consent_text": "I hear by declare my consent agreement for fetching my information via AITAN Labs API"
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "1533020cc6mshd7dfca12905cff6p1cc03ajsn26b9b8b9c9ab",
	"X-RapidAPI-Host": "rto-vehicle-information-verification-india.p.rapidapi.com"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())