import time
import board
import busio
import adafruit_gps
import serial
import csv


uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=3000)
gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

last_print = time.monotonic()

with open("data/nmea.txt", "wb") as nmea, open("data/data.csv", "w") as data:
    fieldnames = ['time', 'latitude', 'longitude', 'speed', 'altitude', 'angle']
    data_writer = csv.DictWriter(data, fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    data_writer.writeheader()
    while True:
        
        gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1.0:
            last_print = current
            
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                print('Waiting for fix...')
                continue

            #NMEA data
            sentence = uart.readline()
            nmea.write(sentence)
            nmea.flush()

            data_writer.writerow({'time': '{:02}:{:02}:{:02}'.format(gps.timestamp_utc.tm_hour, gps.timestamp_utc.tm_min, gps.timestamp_utc.tm_sec),
                'latitude': gps.latitude,
                'longitude': gps.longitude,
                'speed': gps.speed_knots,
                'altitude': gps.altitude_m,
                'angle': gps.track_angle_deg})
            
            # We have a fix! (gps.has_fix is true)
            # Print out details about the fix like location, date, etc.
            print('=' * 40)  # Print a separator line.
            print('Fix timestamp: {:02}:{:02}:{:02}'.format(
                gps.timestamp_utc.tm_hour,
                gps.timestamp_utc.tm_min,   
                gps.timestamp_utc.tm_sec))
            #Print NMEA data written
            print(str(sentence, 'ascii').strip())

            print('Latitude: {0:.6f} degrees'.format(gps.latitude))
            print('Longitude: {0:.6f} degrees'.format(gps.longitude))
            print('Fix quality: {}'.format(gps.fix_quality))
            # Some attributes beyond latitude, longitude and timestamp are optional
            # and might not be present.  Check if they're None before trying to use!
            if gps.satellites is not None:
                print('# satellites: {}'.format(gps.satellites))
            if gps.altitude_m is not None:
                print('Altitude: {} meters'.format(gps.altitude_m))
            if gps.speed_knots is not None:
                print('Speed: {} knots'.format(gps.speed_knots))
            if gps.track_angle_deg is not None:
                print('Track angle: {} degrees'.format(gps.track_angle_deg))