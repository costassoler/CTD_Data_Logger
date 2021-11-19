from kellerLD import KellerLD
sensor = KellerLD()
sensor.init()
sensor.read()
sensor.pressure()
print(sensor.pressure())

