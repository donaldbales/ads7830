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

ref_vol = 2.5
base = float(255 << 8)

while True:
    for i in range(1):
        val = float(analog_inputs[i].value)
        print(f"ADC input {i} = {val}, {((val * ref_vol) / base) * 3.3/2.5}")
    time.sleep(1)

