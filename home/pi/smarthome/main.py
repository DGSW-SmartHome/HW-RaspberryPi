import serial
import paho.mqtt.client as mqtt
import json
import re
import struct
import time

global arduino

def on_connect(client, userdata, flags, rc):
    print('connected')
    client.subscribe('/SMARTHOME')

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload)
    
    try:
        j = json.loads(msg.payload)
        if j['type'] == 'light1':
            if j['cmd'] == 'on':
                arduino.write(b'L1-1')
            else:
                arduino.write(b'L1-0')
        if j['type'] == 'light2':
            if j['cmd'] == 'on':
                arduino.write(b'L2-1')
            else:
                arduino.write(b'L2-0')
        if j['type'] == 'light3':
            if j['cmd'] == 'on':
                arduino.write(b'L3-1')
            else:
                arduino.write(b'L3-0')
        if j['type'] == 'light4':
            if j['cmd'] == 'on':
                arduino.write(b'L4-1')
            else:
                arduino.write(b'L4-0')
        if j['type'] == 'light5':
            if j['cmd'] == 'on':
                arduino.write(b'L5-1')
            else:
                arduino.write(b'L5-0')
        if j['type'] == 'light6':
            if j['cmd'] == 'on':
                arduino.write(b'L6-1')
            else:
                arduino.write(b'L6-0')
        if j['type'] == 'plug1':
            if j['cmd'] == 'on':
                arduino.write(b'O1-1')
            else:
                arduino.write(b'O1-0')
        if j['type'] == 'plug2':
            if j['cmd'] == 'on':
                arduino.write(b'O2-1')
            else:
                arduino.write(b'O2-0')
        if j['type'] == 'plug3':
            if j['cmd'] == 'on':
                arduino.write(b'O3-1')
            else:
                arduino.write(b'03-0')
        if j['type'] == 'plug4':
            if j['cmd'] == 'on':
                arduino.write(b'O4-1')
            else:
                arduino.write(b'O4-0')
        if j['type'] == 'plug5':
            if j['cmd'] == 'on':
                arduino.write(b'O5-1')
            else:
                arduino.write(b'O5-0')
        if j['type'] == 'plug6':
            if j['cmd'] == 'on':
                arduino.write(b'O6-1')
            else:
                arduino.write(b'O6-0')

    except Exception as e:
        print(e)
        pass

address = None

client = mqtt.client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(address, 1883)
client.loop_start()


regex = b'^F(.{4})L1(.{1})L2(.{1})L3(.{1})L4(.{1})L5(.{1})L6(.{1})\n$'
def read_arduino(ser):
    m = re.match(regex, ser.readline())
    if m is not None:
        finedust = struct.unpack('<f', m[1])[0]
        light1 = int.from_bytes(m[2], byteorder='little')
        light2 = int.from_bytes(m[3], byteorder='little')
        light3 = int.from_bytes(m[4], byteorder='little')
        light4 = int.from_bytes(m[5], byteorder='little')
        light5 = int.from_bytes(m[6], byteorder='little')
        light6 = int.from_bytes(m[7], byteorder='little')

        return {
            'finedust': finedust,
            'light1': light1,
            'light2': light2,
            'light3': light3,
            'light4': light4,
            'light5': light5,
            'light6': light6
        }
    else:
        return None


try:
    arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

    arduino.flushInput()
    while True:
        data = read_arduino(arduino)
        if data is not None:
            print('finedust: {finedust} / Light1: {light1} / Light2: {light2} / Light3: {light3} / Light4: {light4} / Light5: {light5} / Light6: {light6}'.format(**data))

            client.publish('/SMARTHOME', json.dumps(data))

        client.loop_read()
        time.sleep(1)


except Exception as e:
    print(e)
    pass
