import time
import board
import adafruit_ads7830.ads7830
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
adc = adafruit_ads7830.ads7830.ADS7830(i2c, 0x48, False, False, False) 
#int_ref_power_down=False, adc_power_down=True)
analog_inputs = []
for i in range(8):
    c = AnalogIn(adc, i)
    analog_inputs.append(c)

ref_volt = 2.5
ls255by8 = float(255 << 8)

while True:
    for i in range(1):
        lsby8val = analog_inputs[i].value
        val = lsby8val >> 8
        print(f"ADC input {i} = {lsby8val}, {((lsby8val * ref_volt) / ls255by8)}, {val}, {((val * ref_volt) / 255)}")
    time.sleep(1)

