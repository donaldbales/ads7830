import time
import board
import adafruit_ads7830.ads7830
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
adc = adafruit_ads7830.ads7830.ADS7830(i2c, 0x48, False, True, True)
analog_inputs = []
for i in range(8):
    c = AnalogIn(adc, i)
    analog_inputs.append(c)

ref_vol = 3.3 # which is VIN on RPi
ls255by8 = float(255 << 8) # the ads7830 lib returns a left shifted by 8 bits value

while True:
    for i in range(1):
        val = float(analog_inputs[i].value)
        print(f"ls255by8 = {ls255by8}, ADC input {i} = {val}, {((val * ref_vol) / ls255by8)}")
    time.sleep(1)

