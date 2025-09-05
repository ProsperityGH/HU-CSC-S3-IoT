import network
import time
import machine
import socket

# WiFi gegevens
SSID = 'Cisco19101'
PASSWORD = 'ciscocisco'


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


def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('Listening on', addr)

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)

        # Lees de hele request inclusief headers
        request_line = cl_file.readline().decode().strip()
        print('Request:', request_line)
        while True:
            header = cl_file.readline().decode().strip()
            if not header:
                break
            print("Header:", header)

        # Response body maken
        body = f'Hi from {machine.unique_id().hex()}, my GPIO0 is {machine.Pin(0).value()}\n'
        body_bytes = body.encode()

        # Response sturen met Content-Length
        cl.send(b'HTTP/1.1 200 OK\r\n')
        cl.send(b'Content-Type: text/plain\r\n')
        cl.send(f'Content-Length: {len(body_bytes)}\r\n'.encode())
        cl.send(b'Connection: close\r\n')
        cl.send(b'\r\n')
        cl.send(body_bytes)

        cl.close()


# Verbinden met WiFi
connect_to_wifi(SSID, PASSWORD)

# Start de webserver
start_web_server()
