from microbit import *
import radio
import utime
import ssd1306
import ssd1306_text

radio.on()
radio.config(group=10)
display.off()
i2c.init(sda=pin20, scl=pin19)
ssd1306.initialize()
ssd1306.clear_oled()
spaces = 10
last_spaces = -1
trig_in, echo_in = pin1, pin2
servo_pin = pin0

def get_distance():
    trig_in.write_digital(0); utime.sleep_us(2)
    trig_in.write_digital(1); utime.sleep_us(10); trig_in.write_digital(0)
    timeout = 30000; start_wait = utime.ticks_us()
    while echo_in.read_digital() == 0:
        if utime.ticks_diff(utime.ticks_us(), start_wait) > timeout: return 999
    t1 = utime.ticks_us()
    while echo_in.read_digital() == 1:
        if utime.ticks_diff(utime.ticks_us(), t1) > timeout: break
    return utime.ticks_diff(utime.ticks_us(), t1) / 58

def update_display(line1, line2=""):
    ssd1306.clear_oled()
    ssd1306_text.add_text(0, 0, line1.replace(" ", "").replace(":", ""))
    if line2: ssd1306_text.add_text(0, 2, line2.replace(" ", "").replace(":", ""))

while True:
    incoming = radio.receive()
    if incoming == "GATE_OUT" and spaces < 10: spaces += 1
    if spaces != last_spaces:
        update_display("SPACE" + str(spaces)); last_spaces = spaces
    if get_distance() < 5:
        if spaces > 0:
            radio.send("IN:" + str(utime.ticks_ms())); spaces -= 1
            update_display("WELCOME"); servo_pin.set_analog_period(20)
            servo_pin.write_analog(100); sleep(3000); servo_pin.write_analog(30)
            last_spaces = -1
        else:
            update_display("FULL", "SORRY"); sleep(2000); last_spaces = -1
    sleep(200)

