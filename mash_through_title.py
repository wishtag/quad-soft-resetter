from PIL import ImageGrab, Image
import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

windows = [[[664,94,957,270], [664,272,957,492]], [[1624,94,1917,270], [1624,272,1917,492]], [[664,607,957,783], [664,785,957,1005]], [[1624,607,1917,783], [1624,785,1917,1005]]]

instances_status = [False,False,False,False]

def press_and_release(button):
    gamepad.press_button(button=button)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=button)
    gamepad.update()

def not_ready(instances_ready):
    if instances_ready[0] == False or instances_ready[1] == False or instances_ready[2] == False or instances_ready[3] == False:
        return True

time.sleep(3)
press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

while not_ready(instances_status):
    time.sleep(0.01)
    for i in range(4):
        if instances_status[i] != True:
            screenshot = ImageGrab.grab(bbox=windows[i][0])
            pixels = screenshot.load()
            screenshot.close()

            r, g, b = pixels[0, 0]
            if r == 0 and g == 0 and b == 0:
                instances_status[i] = True
instances_status = [False,False,False,False]

while not_ready(instances_status):
    time.sleep(0.01)
    for i in range(4):
        if instances_status[i] != True:
            screenshot = ImageGrab.grab(bbox=windows[i][0])
            pixels = screenshot.load()
            screenshot.close()

            r, g, b = pixels[0, 0]
            if r != 0 and g != 0 and b != 0:
                instances_status[i] = True
instances_status = [False,False,False,False]

time.sleep(0.5)
press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)