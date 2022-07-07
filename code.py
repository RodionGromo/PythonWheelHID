import usb_hid
import board,digitalio,time
import wheel
import random
buttons = [0,0,0,0,0,0]
analogs = [0,0,0,0]

# button = digitalio.DigitalInOut(board.GP11)
# button.direction = digitalio.Direction.INPUT
# power = digitalio.DigitalInOut(board.GP10)
# power.direction = digitalio.Direction.OUTPUT
# power.value = True

wheel = wheel.gameWheel(usb_hid.devices)
pressed = False

while True:
    if(pressed):
        wheel.press_buttons((0,1,2,3,4,5,6))
    else:
        wheel.release_buttons((0,1,2,3,4,5,6))
    pressed = not pressed
    wheel.move_analogs(a1=random.randint(-100,100),a2=random.randint(-100,100),a3=random.randint(-100,100),a4=random.randint(-100,100))
    time.sleep(0.5)


