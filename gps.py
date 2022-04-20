import serial
import sys
import pynmea2
from time import sleep


grep_res = sys.stdin
grep_str = grep_res.read().strip()

if not ('tty' in grep_str):
    print('Wrong')
    exit(-1)

port_name = '/dev/tty' + grep_str.split('tty')[1].split(':')[0]
print('port name: ', port_name)

ser = None
print(f'try to connect device via serial port {port_name}')
try:
    ser = serial.Serial(port=port_name, baudrate=9600, timeout=1)
except (serial.serialutil.SerialException):
    print('Connection failed...')
    exit(-1)

print('Connection success')

#f = open('../gps.txt', 'w')
while True:
    latitude, longitude = 0, 0
    msg = ''
    try:
        line = str(ser.readline(), 'utf-8')
        msg = pynmea2.parse(line)
        latitude = msg.latitude
        longitude = msg.longitude

        #print(f'lat={latitude}, lon={longitude}')
        # write lat and long to file
        with open('../gps.txt', 'w') as f:
            f.write(f'lat,long={latitude},{longitude}')
            print(f'lat={latitude}, lon={longitude}')
            f.close()
    except (AttributeError):
        pass
    except (KeyboardInterrupt):
        ser.close()
        exit(0)
