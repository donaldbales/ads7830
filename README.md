# ads7830
### Adafruit ADS7830 8-bit ADC and Raspberry Pi 3 experiments

This product can be found at: https://www.adafruit.com/product/5836

From there, you can find the tutorial at: https://learn.adafruit.com/adafruit-ads7830-8-channel-8-bit-adc

The data sheet for the ADS7830 can be found at: https://www.ti.com/lit/ds/symlink/ads7830.pdf

Personaly, I found the product page and tutorial a bit vague about the reference voltage. Especially the example code:

```
# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo to read analog input on channel 0

import time

import board

import adafruit_ads7830.ads7830 as ADC
from adafruit_ads7830.analog_in import AnalogIn

i2c = board.I2C()

# Initialize ADS7830
adc = ADC.ADS7830(i2c)
chan = AnalogIn(adc, 0)

while True:
    print(f"ADC channel 0 = {chan.value}")
    time.sleep(0.1)
```

So here's what I learned through experimentation.

## Using the Default Reference Voltage

By default, the reference voltage is tied to Vin, which is 3.3V when hooked up to the I2C bus on a Raspberry Pi 3.

In the example code above, There's what I believe to be a mistake. The default value for the ADS7830 class sets the parameter int_ref_power_down=False. 

```
# Initialize ADS7830
adc = ADC.ADS7830(i2c)
```

This sets the bit PD1 in the command byte to 1, which turns on the internal 2.5V referencce voltage. But Vin, 3.3V from the I2C connection is already tied to it. The result? Inaccurate voltage readings.

To get accurate voltage readings using the default Vin, 3.3V, reference voltage, I needed to pass int_ref_power_down=True to the initializer:

```
# Initialize ADS7830
adc = ADC.ADS7830(i2c, int_ref_power_down=True)
```

Of course, you can pass this parameter positionally:

```
# Initialize ADS7830
adc = ADC.ADS7830(i2c, 0x48, False, True)
```

## Using the Internal Reference Voltage

In order to use the internal 2.5V reference voltage, you need to cut the **Ext Ref** trace on the back side of the PCB board.

Then, you can use the default initializer:

```
# Initialize ADS7830
adc = ADC.ADS7830(i2c)
```

The default initializer sets the internal reference on by default.

## Calculating Voltage Values

You can calculate the voltage by using the following formula:

```
voltage = channel value * reference voltage / left shift 255 by 8
```

**Channel value** is the value returned by the *Adafruit_CircuitPython_ADS7830* library. The ADS7830 is an 8-bit analog to digital converter, so its hardware's returned value will be between: 0 - 255. The *Adafruit_CircuitPython_ADS7830* library, by design, returns the 0 - 255 value left shifted by 8-bits in order to make the returned channel value a value between: 0 - 65535, a 16-bit value. This means the divisor of the formula above has to be the value 255 shifted left by 8-bits (65280).

**Reference voltage** is the reference value for your implementation. That's 3.3V by default, or 2.5V if you use the internal reference voltage (remember to cut the trace).

**Left shift 255 by 8** is the maximum possible channel value, The hardware uses 255. But the library returns the value left shifted by 8-bits, so this divisor value must be left shifted by 8-bits, which equals 65280.




