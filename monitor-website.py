import requests
import smtplib
import os
# import dotenv

# dotenv.load_dotenv()

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
PASSKEY = os.environ.get('EMAIL_PASS')
SERVER = os.environ.get('SERVER')

def send_notification(email_msg):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, PASSKEY)
        message = f"Subject: Website Not accessible Alert\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
try: 
    response = requests.get('http://{SERVER}:8080/')
    if response.status_code == 200:
        print("Website is up and running!")
    else:
        print("Website is down or not reachable")
        msg = f"Website returned status code: {response.status_code}"
        send_notification(msg)

except Exception as ex:
    print(f'Connection error happened: {ex}')
    msg = f"An error occurred: {ex}"
    send_notification(msg)
    
