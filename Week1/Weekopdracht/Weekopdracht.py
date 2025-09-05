import network
import time
import machine
import urequests
import ubinascii

# WiFi gegevens
SSID = 'Cisco19101'
PASSWORD = 'ciscocisco'

# Server endpoint
URL = "https://csc-sem3-jan.westeurope.cloudapp.azure.com/goapp/register"

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    print('Connecting to Wi-Fi...')
    while not wlan.isconnected():
        print('.', end='')
        time.sleep(1)

    print('\nConnected to Wi-Fi')
    print('Network config:', wlan.ifconfig())
def data():
    hardware_id = ubinascii.hexlify(machine.unique_id()).decode()

    payload = {
        "id": 3, 
        "hardware_id": hardware_id,
        "email1": "Prosper@hu.nl",
        "email2": "Leon@hu.nl"
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = urequests.post(URL, json=payload, headers=headers)
        print("Status:", response.status_code)
        print("Response:", response.text)
        response.close()
    except Exception as e:
        print("Error sending data:", e)


# Verbinden met WiFi
connect_to_wifi(SSID, PASSWORD)

# Data sturen
data()