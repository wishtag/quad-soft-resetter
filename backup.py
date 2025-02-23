import os
from PIL import ImageGrab, Image
import pyautogui
import time
import pydirectinput
from datetime import datetime, date
from pytz import timezone
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore, Style
import vgamepad as vg

gamepad = vg.VX360Gamepad()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_json(file):
    f = open (file, "r")
    data = json.loads(f.read())
    f.close()
    return data

def write_json(file, object):
    f = open (file, "w")
    json.dump(object, f)
    f.close()

def press_and_release(button):
    gamepad.press_button(button=button)
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=button)
    gamepad.update()

window_1 = [[664,94,957,270], [664,272,957,492]]
window_2 = [[0,94,0,270], [0,272,0,492]]
window_3 = [[664,0,957,0], [664,0,957,0]]

debug = False
json_time = read_json("resets.json")["total_seconds"]
delay = 0
is_shiny = False
name = "Pheromosa"
webhook_url = ""

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

try:
    os.remove('img/screenshot.png')
except:
    pass

clear_screen()
temp = read_json("resets.json")["last_delay"]
print(f"Would you like to reset {Fore.GREEN}[last_delay]{Style.RESET_ALL}? Current value is: {Fore.GREEN}{temp}{Style.RESET_ALL}")
choice = input("[y/n]: ")
if choice == "y" or choice == "Y":
    resets = read_json("resets.json")
    resets["last_delay"] = 0
    write_json("resets.json", resets)


for i in range(5,0,-1):
    clear_screen()
    print(i)
    time.sleep(1)
clear_screen()

#if debug:
#    print("Focusing game...")

#temp = 0
#while True: #waiting for x to be black (focusing window)
#    screenshot = ImageGrab.grab(bbox=(1895,14,1897,16))
#    pixels = screenshot.load()
#    screenshot.close()
#
#    r, g, b = pixels[0, 0]
#    if r == 155 and g == 156 and b == 156:
#        temp = temp + 1
#        pyautogui.keyDown('alt')
#        for i in range(temp):
#            pyautogui.press('tab')
#        pyautogui.keyUp('alt')
#        time.sleep(1)
#    else:
#        break

#if debug:
#    print("Focused!")

while is_shiny == False:
    delay = 0

    if debug:
        print("Waiting for encounter to be interactable (waiting for screen to not be black)...")

    while True:
        time.sleep(0.01)
        screenshot = ImageGrab.grab(bbox=(1025,53,1855,551))
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[0, 0]
        if r != 0 and g != 0 and b != 0:
            break
    
    if debug:
        print("Encounter interactable! (screen not black)")

    time.sleep(0.5)
    press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

    if debug:
        print("Interact input sent")

    if debug:
        print("Waiting for encounter transition to begin (bottom screen turning black)...")

    while True: #waiting for the bottom screen to turn black
        time.sleep(0.01)
        screenshot = ImageGrab.grab(bbox=(1108,551,1772,1050))
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[0, 0]
        if r == 0 and g == 0 and b == 0:
            break

    if debug:
        print("Encounter transition begun!")

    if debug:
        print("Waiting for encounter to begin (bottom screen turning any color other than black)...")

    while True: #waiting for the bottom screen to be any color but black
        time.sleep(0.01)
        screenshot = ImageGrab.grab(bbox=(1108,551,1772,1050))
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[0, 0]
        if r != 0 and g != 0 and b != 0:
            break
    
    if debug:
        print("Encounter begun!")

    hour = datetime.now(timezone('US/Central')).hour
    minute = datetime.now(timezone('US/Central')).minute
    second = datetime.now(timezone('US/Central')).second
    current_time = (hour*60**2) + (minute*60) + second
    elapsed_time = current_time - start_time
    resets = read_json("resets.json")
    resets["resets"] = resets["resets"] + 1
    resets["total_seconds"] = json_time + elapsed_time
    write_json("resets.json", resets)

    if debug:
        print("Waiting for introduction animation to end (waiting for a blue pixel from the battle UI to appear on screen)...")

    while True:
        time.sleep(0.01)
        delay = delay + 1
        if delay == 80:
            encounter = ImageGrab.grab(bbox=(1025,53,1855,551))
        screenshot = ImageGrab.grab(bbox=(1025,439,1027,441))
        pixels = screenshot.load()
        screenshot.close()

        r, g, b = pixels[0, 0]
        if r == 0 and g == 157 and b == 174:
            break
    
    if debug:
        print("Encounter introduction ended!")

    if debug:
        print("Comparing delays...")

    last_delay = read_json("resets.json")["last_delay"]
    if last_delay == 0:
        resets = read_json("resets.json")
        resets["last_delay"] = delay
        write_json("resets.json", resets)
    
    last_delay = read_json("resets.json")["last_delay"]
    print(abs(last_delay-delay))
    if abs(last_delay-delay) > 15:
        encounter.save("img/screenshot.png")
        encounter.close()

        if debug:
            print("Longer delay in encounter")

        is_shiny = True
        #pyautogui.hotkey('ctrl', 'c')

        #if debug:
        #    print("Save state created")

        resets = read_json("resets.json")

        seconds = resets["total_seconds"]

        in_minutes = seconds / 60

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

        webhook = DiscordWebhook(url=webhook_url, username="Sparkles")
        with open("img/screenshot.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="screenshot.png")
        embed = DiscordEmbed(title=f"Shiny {name} Found", description=f"{resets['resets']} resets over the span of {time_formatted}", color="FCDE3A")
        embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
        embed.set_image(url="attachment://screenshot.png")
        embed.add_embed_field(name="Total Time in Minutes", value=str(in_minutes))
        embed.set_footer(text="Ultra Moon")
        embed.set_timestamp()
        webhook.add_embed(embed)
        response = webhook.execute()

        resets["last_delay"] = delay
        write_json("resets.json", resets)
    else:
        #webhook = DiscordWebhook(url=webhook_url, username="Sparkles")
        #embed = DiscordEmbed(title=f"Not Shiny", description="Placeholder", color="FCDE3A")
        #embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
        #webhook.add_embed(embed)
        #webhook.execute()

        if debug:
            print("Normal encounter delay")
            print("Softresetting...")

        resets = read_json("resets.json")
        resets["last_delay"] = delay
        write_json("resets.json", resets)

        encounter.close()
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()
        time.sleep(0.1)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        gamepad.update()

        if debug:
            print("Waiting for title screen to appear (waiting for the top screen to be white)...")

        while True:
            time.sleep(0.01)
            screenshot = ImageGrab.grab(bbox=(1052,474,1191,506))
            pixels = screenshot.load()
            screenshot.close()

            r, g, b = pixels[1, 1]
            if r == 255 or g == 255 or b == 255:
                break
        
        if debug:
            print("Title screen appeared!")

        time.sleep(0.5)
        press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

        if debug:
            print("Interact input sent")

        if debug:
            print("Waiting for save selection to appear (waiting for a yellow pixel on the trainer card to appear)...")

        while True:
            time.sleep(0.01)
            screenshot = ImageGrab.grab(bbox=(1732,196,1734,198))
            pixels = screenshot.load()
            screenshot.close()

            r, g, b = pixels[1, 1]
            if r == 255 and g == 215 and b == 53:
                break
        if debug:
            print("Save selection appeared!")
        
        time.sleep(0.5)
        press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

        if debug:
            print("Interact input sent")

        if debug:
            print("Waiting for screen to turn black")
        
        while True:
            time.sleep(0.01)
            screenshot = ImageGrab.grab(bbox=(1025,53,1855,551))
            pixels = screenshot.load()
            screenshot.close()

            r, g, b = pixels[0, 0]
            if r == 0 and g == 0 and b == 0:
                break
        
        if debug:
            print("Screen is black!")