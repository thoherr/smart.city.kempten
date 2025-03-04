from machine import ADC

_temperature_sensor = ADC(4)

def value():
    adc_value = _temperature_sensor.read_u16()
    voltage = adc_value * (3.3 / 65535.0)
    return round(27 - (voltage - 0.706) / 0.001721, 1)
