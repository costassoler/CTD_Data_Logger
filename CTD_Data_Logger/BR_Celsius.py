import tsys01
sensor = tsys01.TSYS01()
sensor.init()
sensor.read()

T = sensor.temperature()
print(T)
