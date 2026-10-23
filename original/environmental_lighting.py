from microbit import *

OFF = 1023
NIGHT_THRESHOLD = 260
color_pos = 0

def get_base_color(pos):
    if pos < 85: return int(pos / 85 * 1023), int((85 - pos) / 85 * 1023), 0
    if pos < 170:
        pos -= 85; return int((85 - pos) / 85 * 1023), 0, int(pos / 85 * 1023)
    pos -= 170; return 0, int(pos / 85 * 1023), int((85 - pos) / 85 * 1023)

while True:
    current_light = pin0.read_analog()
    if current_light > NIGHT_THRESHOLD:
        display.show(Image.HAPPY); brightness = pin1.read_analog() / 1023.0
        base_r, base_g, base_b = get_base_color(color_pos)
        pin2.write_analog(1023 - int(base_r * brightness))
        pin16.write_analog(1023 - int(base_g * brightness))
        pin8.write_analog(1023 - int(base_b * brightness))
        color_pos = (color_pos + 2) % 256
    else:
        display.clear(); pin2.write_analog(OFF); pin16.write_analog(OFF); pin8.write_analog(OFF)
    sleep(50)

