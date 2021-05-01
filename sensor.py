import adafruit_dht
from board import D4
import time
import pickle
import socket

SERVER = '192.168.1.85'
PORT = 2003
dht_device = adafruit_dht.DHT22(D4)

while True:
    try:
        temperature = dht_device.temperature
        temp_f = round(temperature * (9 / 5) + 32, 2)
        humidity = dht_device.humidity
    except (RuntimeError, OSError) as e:
        time.sleep(2.5)
        continue
    except Exception as error:
        dht_device.exit()
        raise error
    timestamp = int(time.time())
    lines = ['local.office.temp {0} {1}'.format(temp_f, timestamp), 'local.office.humidity {0} {1}'.format(humidity, timestamp)]
    message = '\n'.join(lines) + '\n'
    while True:
        try:
            sock = socket.socket()
            sock.connect((SERVER, PORT))
            sock.sendall(message.encode('utf-8'))
            sock.close
            break
        except OSError as error:
            time.sleep(1)
            continue
    time.sleep(2.5)
