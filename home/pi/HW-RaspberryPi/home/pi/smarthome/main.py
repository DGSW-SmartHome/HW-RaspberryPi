import serial
import paho.mqtt.client as mqtt
import json
import re
import struct
import time

global arduino

def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('/SMARTHOME/control')

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)

    try:
        j = json.loads(msg.payload)
        if j['type'] == 'light1':
            if j['cmd'] == 0:
                arduino.write('L1-0'.encode(encoding="utf-8"))
            elif j['cmd'] == 1:
                arduino.write('L1-1'.encode(encoding="utf-8"))
            elif j['cmd'] == 2:
                arduino.write('L1-2'.encode(encoding="utf-8"))
            elif j['cmd'] == 3:
                arduino.write('L1-3'.encode(encoding="utf-8"))
        if j['type'] == 'light2':
            if j['cmd'] == 0:
                arduino.write('L2-0'.encode(encoding="utf-8"))
            elif j['cmd'] == 1:
                arduino.write('L2-1'.encode(encoding="utf-8"))
            elif j['cmd'] == 2:
                arduino.write('L2-2'.encode(encoding="utf-8"))
            elif j['cmd'] == 3:
                arduino.write('L2-3'.encode(encoding="utf-8"))
        if j['type'] == 'light3':
            if j['cmd'] == 0:
                arduino.write('L3-0'.encode(encoding="utf-8"))
            elif j['cmd'] == 1:
                arduino.write('L3-1'.encode(encoding="utf-8"))
            elif j['cmd'] == 2:
                arduino.write('L3-2'.encode(encoding="utf-8"))
            elif j['cmd'] == 3:
                arduino.write('L3-3'.encode(encoding="utf-8"))
        if j['type'] == 'plug1':
            if j['cmd'] == 'on':
                arduino.write('O1-1'.encode(encoding="utf-8"))
            else:
                arduino.write('O1-0'.encode(encoding="utf-8"))
        if j['type'] == 'plug2':
            if j['cmd'] == 'on':
                arduino.write('O2-1'.encode(encoding="utf-8"))
            else:
                arduino.write('O2-0'.encode(encoding="utf-8"))
        if j['type'] == 'plug3':
            if j['cmd'] == 'on':
                arduino.write('O3-1'.encode(encoding="utf-8"))
            else:
                arduino.write('03-0'.encode(encoding="utf-8"))

    except Exception as e:
        print(e)
        pass

address = '13.209.41.37'

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(address, 1883)
client.loop_start()


regex = b'^F(.{4})L1(.{1})L2(.{1})L3(.{1})\n$'
def read_arduino(ser):
    m = re.match(regex, ser.readline())
    if m is not None:
        finedust = struct.unpack('<f', m[1])[0]
        light1 = int.from_bytes(m[2], byteorder='little')
        light2 = int.from_bytes(m[3], byteorder='little')
        light3 = int.from_bytes(m[4], byteorder='little')

        print(light1, light2, light3)
        return {
            'finedust': finedust,
            'light1': light1,
            'light2': light2,
            'light3': light3
        }
    else:
        return None


try:
    arduino = serial.Serial('/dev/ttyUSB1', 115200, timeout=1)

    while True:
        arduino.flushInput()
        data = read_arduino(arduino)
        if data is not None:
            print('finedust: {finedust} / Light1: {light1} / Light2: {light2} / Light3: {light3}'.format(**data))

            client.publish('/SMARTHOME/sensor', json.dumps(data))

        client.loop_read()
        time.sleep(1)


except Exception as e:
    print(e)
    pass
