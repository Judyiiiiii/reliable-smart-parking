from microbit import *
import machine
import music
import neopixel

display.off()
power_l1_r, power_l1_g, power_l2_r, power_l2_g = pin4, pin6, pin13, pin14
for p in (power_l1_r, power_l1_g, power_l2_r, power_l2_g): p.write_digital(1)
trig1, echo1, led1_red, led1_green = pin0, pin1, pin2, pin3
trig2, echo2, led2_red, led2_green = pin8, pin9, pin10, pin12
for p in (led1_red, led1_green, led2_red, led2_green): p.write_digital(1)
np = neopixel.NeoPixel(pin16, 30)

def get_distance(trig, echo):
    trig.write_digital(0); sleep(2); trig.write_digital(1); sleep(10); trig.write_digital(0)
    duration = machine.time_pulse_us(echo, 1, 30000)
    return duration * 0.034 / 2 if duration > 0 else 999

while True:
    alarm_triggered = False; spot1_empty = False; spot2_empty = False
    dist1 = get_distance(trig1, echo1)
    if 0 < dist1 < 10:
        led1_red.write_digital(0); led1_green.write_digital(1)
        if dist1 <= 2.5: alarm_triggered = True
    else:
        led1_red.write_digital(1); led1_green.write_digital(0); spot1_empty = True
    sleep(50)
    dist2 = get_distance(trig2, echo2)
    if 0 < dist2 < 10:
        led2_red.write_digital(0); led2_green.write_digital(1)
        if dist2 <= 2.5: alarm_triggered = True
    else:
        led2_red.write_digital(1); led2_green.write_digital(0); spot2_empty = True
    green, red = (0, 20, 0), (20, 0, 0)
    for i in range(30): np[i] = (0, 0, 0)
    for i in range(15): np[i] = red
    if spot1_empty and spot2_empty:
        for i in range(15, 30): np[i] = green
    elif spot1_empty:
        for i in range(15, 23): np[i] = green
    elif spot2_empty:
        for i in range(23, 30): np[i] = green
    else:
        for i in range(15, 30): np[i] = red
    np.show()
    if alarm_triggered: music.play(music.WAWAWAWAA, pin=pin15, wait=False); sleep(400)
    else: sleep(450)

