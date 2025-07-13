import requests
import smtplib
import os
import paramiko
import linode_api4
import time
import schedule
# import dotenv

# dotenv.load_dotenv()

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
PASSKEY = os.environ.get('EMAIL_PASS')
SERVER = os.environ.get('SERVER')
USER = os.environ.get('USER')
SSH_KEY = os.environ.get('SSH_KEY')
LINODE_TOKEN = os.environ.get('LINODE_TOKEN')
LINODE_ID = os.environ.get('LINODE_ID')
HOSTNAME = os.environ.get('HOSTNAME')




def restart_server_and_app():
    # Restart server
    print('Rebooting the server .....')
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    server_nginx = client.load(linode_api4.Instance, LINODE_ID)
    server_nginx.reboot()
    print('Server rebooted')

    # Restart the app
    while True:
        server_nginx = client.load(linode_api4.Instance, LINODE_ID)
        if server_nginx.status == 'running':
            time.sleep(5)
            restart_container()
            break

def send_notification(email_msg):
    print('Sending an email.....')
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS, PASSKEY)
        message = f"Subject: Website Not accessible Alert\n{email_msg}"
        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)

def restart_container():
    print("Restarting the application.....")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=HOSTNAME, username=USER, key_filename=SSH_KEY)
    stdout = ssh.exec_command('docker start 57242dd585f9')
    print(stdout.readlines())
    ssh.close()
    print('Application restarted')
    
def monitor_application():     
    try: 
        response = requests.get(SERVER)
        if response.status_code == 200:
            print("Website is up and running!")
        else:
            print("Website is down or not reachable")
            msg = f"Website returned status code: {response.status_code}"
            send_notification(msg)
            
            #restart the application server
            restart_container()
        

    except Exception as ex:
        print(f'Connection error happened: {ex}')
        msg = f"An error occurred: {ex}"
        send_notification(msg)
        restart_server_and_app()
    
schedule.every(5).seconds.do(monitor_application)

while True:
    schedule.run_pending()
    

    
    