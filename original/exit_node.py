from microbit import *
import radio
import utime
import ssd1306
import ssd1306_text

radio.on(); radio.config(group=10); display.off()
i2c.init(sda=pin20, scl=pin19); ssd1306.initialize(); ssd1306.clear_oled()
trig_out, echo_out = pin1, pin2
servo_pin = pin0
entry_time = 0

def get_distance():
    trig_out.write_digital(0); utime.sleep_us(2)
    trig_out.write_digital(1); utime.sleep_us(10); trig_out.write_digital(0)
    timeout = 30000; start_wait = utime.ticks_us()
    while echo_out.read_digital() == 0:
        if utime.ticks_diff(utime.ticks_us(), start_wait) > timeout: return 999
    t1 = utime.ticks_us()
    while echo_out.read_digital() == 1:
        if utime.ticks_diff(utime.ticks_us(), t1) > timeout: break
    return utime.ticks_diff(utime.ticks_us(), t1) / 58

def update_display(line1, line2=""):
    ssd1306.clear_oled(); ssd1306_text.add_text(0, 0, line1.replace(" ", "").replace(":", ""))
    if line2: ssd1306_text.add_text(0, 2, line2.replace(" ", "").replace(":", ""))

update_display("EXITGATE", "READY")
while True:
    incoming = radio.receive()
    if incoming and incoming.startswith("IN:"):
        try: entry_time = int(incoming.split(":")[1])
        except ValueError: pass
    if get_distance() < 5:
        duration_sec = utime.ticks_diff(utime.ticks_ms(), entry_time) // 1000
        update_display("STAYED", str(duration_sec) + "SEC"); radio.send("GATE_OUT")
        servo_pin.set_analog_period(20); servo_pin.write_analog(100)
        sleep(3000); servo_pin.write_analog(30); sleep(1000)
        update_display("EXITGATE", "READY")
    sleep(200)

