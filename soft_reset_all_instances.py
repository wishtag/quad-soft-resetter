import vgamepad as vg
import time

gamepad = vg.VX360Gamepad()

time.sleep(2)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
gamepad.update()
time.sleep(0.1)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
gamepad.update()