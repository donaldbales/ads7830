# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo to read analog input on channel 0

import time

import board

import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
#adc = ADC.ADS7830(i2c, differential_mode=False, int_ref_power_down=False, adc_power_down=False)
adc = ADC.ADS7830(i2c, 0x48, False, False, False)
chan = AnalogIn(adc, 0)

while True:
    value = float(chan.value)
    print(f"ADC channel 0 = {value}, {(value * 2.500) / 255.0}")
    time.sleep(1)
