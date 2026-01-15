# hardware.py
from machine import ADC, Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import config

class SoilMoistureSensor:
    def __init__(self, pin):
        self.adc = ADC(Pin(pin))

    def read_raw(self):
        return self.adc.read_u16()

class PIRMotionSensor:
    def __init__(self, pin):
        self.pin = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        
    def motion_detected(self):
        return self.pin.value() == 1

class ServoIndicator:
    def __init__(self, pin, freq, pos_dry, pos_ok, pos_wet):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(freq)
        self.pos_dry = pos_dry
        self.pos_ok = pos_ok
        self.pos_wet = pos_wet
        self.set_ok()

    def set_dry(self):
        self.pwm.duty_u16(self.pos_dry)

    def set_ok(self):
        self.pwm.duty_u16(self.pos_ok)

    def set_wet(self):
        self.pwm.duty_u16(self.pos_wet)

class OledDisplay:
    def __init__(self, width, height, freq):
        i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=freq)
        print("I2C Address : " + hex(i2c.scan()[0]).upper())
        print("I2C Configuration: " + str(i2c))
        self.display = SSD1306_I2C(width, height, i2c)
        self.width = width

    def show(self, moisture_percent, status_message):
        self.display.fill(0)
        self.display.text("Bodemvochtigheid", 1, 15)
        self.display.text("%.2f %%" % moisture_percent, 35, 35)
        char_width = 8
        text_width = len(status_message) * char_width
        status_x = (self.width - text_width) // 2
        self.display.text(status_message, status_x, 50)
        self.display.show()

    def clear(self):
        self.display.fill(0)
        self.display.show()
