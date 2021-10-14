from random import randint
import time
import socket

'''
Example program for controlling LEDs via WLED
https://kno.wled.ge
'''

API_ENDPOINT = ('192.168.179.15', 21324)
print(f'Connect to {API_ENDPOINT}')

NUM_LEDS = 50
print(f'number of LEDs {NUM_LEDS}')

'''
https://kno.wled.ge/interfaces/udp-realtime/
Byte 0 of the UDP packet tells the server which realtime protocol to use.
Value 	Description 	Max. LEDs
1 	WARLS 	255
2 	DRGB 	490
3 	DRGBW 	367
4 	DNRGB 	489/packet
0 	WLED Notifier 	-
'''
PROTO_WARLS = 1
PROTO_DRGB = 2
PROTO_DRGBW = 4
PROTO_DNRGB = 3
PROTO_WLED_NOTIFIER = 0
PROTO_WAIT_TIME = 50 # seconds

FPS = 50

print(f'running with {FPS} FPS')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pos = 0

while True:
    start_time = time.time()
    data = [PROTO_WARLS, PROTO_WAIT_TIME]
    for i in range(NUM_LEDS):
        data.append(i)

        data.append(2*i) # red
        data.append(255-2*i) # green
        data.append(255 if i==pos else 0) # blue

    sock.sendto(bytes(data), API_ENDPOINT)
    sleep_time = (1/FPS) - (time.time() - start_time)
    pos = (pos  + 1) % NUM_LEDS
    if sleep_time > 0:
        time.sleep(sleep_time)
    else:
        print('FPS too high!')
