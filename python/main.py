import os
from PIL import ImageGrab
import time
from datetime import datetime
from pytz import timezone
import json
from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore, Style
import vgamepad as vg

gamepad = vg.VX360Gamepad()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def read_json(file):
    with open(os.path.abspath(file), 'r') as f:
        data = json.loads(f.read())
    return data

def write_json(file, object):
    with open(os.path.abspath(file), 'w') as f:
        json.dump(object, f)

def press_and_release(button):
    gamepad.press_button(button=eval(buttons[button]))
    gamepad.update()
    time.sleep(0.1)
    gamepad.release_button(button=eval(buttons[button]))
    gamepad.update()

def not_ready(instances_ready):
    if instances_ready[0] == False or instances_ready[1] == False or instances_ready[2] == False or instances_ready[3] == False:
        return True
    
def print_delays(delays):
    clear_screen()
    for i in range(len(delays)):
        print(f"delay{i+1}: {delays[i]}")

window_1 = [[664,94,957,270], [664,272,957,492], [1,94,664,492]]
window_2 = [[1624,94,1917,270], [1624,272,1917,492], [961,94,1624,492]]
window_3 = [[664,607,957,783], [664,785,957,1005], [1,607,664,1005]]
window_4 = [[1624,607,1917,783], [1624,785,1917,1005], [961,607,1624,1005]]
windows = [window_1, window_2, window_3, window_4]

instances_status = [False,False,False,False]
debug = True

resets = read_json("./resets.json")
settings = read_json("./settings.json")

json_time = resets["total_seconds"]
buttons = settings["buttons"]
discord = settings["discord"]
delays = [0,0,0,0]
encounters = [0,0,0,0]
is_shiny = False

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

try:
    os.remove(os.path.abspath("./screenshot.png"))
except:
    pass

clear_screen()
print(f"Would you like to reset {Fore.GREEN}[last_delays]{Style.RESET_ALL}? Current values are: {Fore.GREEN}{resets['last_delays']}{Style.RESET_ALL}")
choice = input("[y/n]: ")
if choice == "y" or choice == "Y":
    resets["last_delays"] = [0,0,0,0]
    write_json("./resets.json", resets)


for i in range(5,0,-1):
    clear_screen()
    print(i)
    time.sleep(1)
clear_screen()

while is_shiny == False:
    delays = [0,0,0,0]

    for i in range(4):
        try:
            encounters[i].close()
        except:
            pass

    if debug:
        print("Waiting for encounter to be interactable (waiting for screen to not be black)...")

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
    
    if debug:
        print("Encounter interactable! (screen not black)")

    time.sleep(0.5)
    press_and_release("A")

    if debug:
        print("Interact input sent")

    if debug:
        print("Waiting for encounter transition to begin (bottom screen turning black)...")

    while not_ready(instances_status):
        time.sleep(0.01)
        for i in range(4):
            if instances_status[i] != True:
                screenshot = ImageGrab.grab(bbox=windows[i][1])
                pixels = screenshot.load()
                screenshot.close()

                r, g, b = pixels[0, 0]
                if r == 0 and g == 0 and b == 0:
                    instances_status[i] = True
    instances_status = [False,False,False,False]

    if debug:
        print("Encounter transition begun!")

    if debug:
        print("Waiting for encounter to begin (bottom screen turning any color other than black)...")

    while not_ready(instances_status):
        time.sleep(0.01)
        for i in range(4):
            if instances_status[i] != True:
                print_delays(delays)
                screenshot = ImageGrab.grab(bbox=windows[i][1])
                pixels = screenshot.load()
                screenshot.close()

                r, g, b = pixels[0, 0]
                if r != 0 and g != 0 and b != 0:
                    instances_status[i] = True
            else:
                delays[i] = delays[i] + 1
                print_delays(delays)
    instances_status = [False,False,False,False]
    
    if debug:
        print("Encounter begun!")

    hour = datetime.now(timezone('US/Central')).hour
    minute = datetime.now(timezone('US/Central')).minute
    second = datetime.now(timezone('US/Central')).second
    current_time = (hour*60**2) + (minute*60) + second
    elapsed_time = current_time - start_time
    resets = read_json("./resets.json")
    resets["resets"] = resets["resets"] + 4
    resets["total_seconds"] = json_time + elapsed_time
    write_json("./resets.json", resets)

    if debug:
        print("Waiting for introduction animation to end (waiting for a green pixel from the battle UI to appear on screen)...")

    while not_ready(instances_status):
        time.sleep(0.01)
        for i in range(4):
            if instances_status[i] != True:
                delays[i] = delays[i] + 1
                print_delays(delays)
                if delays[i] == 30:
                    encounters[i] = ImageGrab.grab(bbox=windows[i][2])
                screenshot = ImageGrab.grab(bbox=windows[i][0])
                pixels = screenshot.load()
                screenshot.close()

                r, g, b = pixels[4, 135]
                if r == 255 and g == 68 and b == 34:
                    instances_status[i] = True
    instances_status = [False,False,False,False]
    
    if debug:
        print("Encounter introduction ended!")

    if debug:
        print("Comparing delays...")

    resets = read_json("./resets.json")
    for i in range(len(resets["last_delays"])):
        if resets["last_delays"][i] == 0:
            resets["last_delays"][i] = delays[i]
    write_json("./resets.json", resets)
    

    avg = (delays[0]+delays[1]+delays[2]+delays[3])/4
    for i in range(4):
        if abs(avg-delays[i]) < 3:
            instances_status[i] = True

    resets = read_json("./resets.json")
    for i in range(len(resets["last_delays"])):
        print(abs(resets["last_delays"][i]-delays[i]))
        if abs(resets["last_delays"][i]-delays[i]) > 8:
            if not_ready(instances_status):
                encounters[i].save(os.path.abspath("./screenshot.png"))
                for i in range(4):
                    try:
                        encounters[i].close()
                    except:
                        pass

                if debug:
                    print("Longer delay in encounter")

                is_shiny = True

                resets = read_json("./resets.json")

                seconds = resets["total_seconds"]

                in_minutes = seconds / 60

                hours = seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = seconds % 60
                time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

                webhook = DiscordWebhook(url=discord["url"], username=discord["name"])
                with open(os.path.abspath("./screenshot.png"), "rb") as f:
                    webhook.add_file(file=f.read(), filename="screenshot.png")
                embed = DiscordEmbed(title=f"Shiny {settings['encounter_name']} Found", description=f"{resets['resets']} resets over the span of {time_formatted} on instance {i+1}", color="FCDE3A")
                embed.set_author(name="Shiny Found", icon_url=discord["icon"])
                embed.set_image(url="attachment://screenshot.png")
                embed.add_embed_field(name="Total Time in Minutes", value=str(in_minutes))
                embed.set_footer(text=discord["game"])
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()

                resets["last_delays"] = delays
                write_json("./resets.json", resets)
    if is_shiny == False:
        instances_status = [False,False,False,False]

        if debug:
            print("Normal encounter delay")
            print("Softresetting...")

        resets = read_json("./resets.json")
        resets["last_delays"] = delays
        write_json("./resets.json", resets)

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

        while not_ready(instances_status):
            time.sleep(0.01)
            for i in range(4):
                if instances_status[i] != True:
                    screenshot = ImageGrab.grab(bbox=windows[i][0])
                    pixels = screenshot.load()
                    screenshot.close()

                    r, g, b = pixels[0, 0]
                    if r == 255 and g == 255 and b == 255:
                        instances_status[i] = True
        instances_status = [False,False,False,False]
        
        if debug:
            print("Title screen appeared!")

        time.sleep(0.5)
        press_and_release("A")

        if debug:
            print("Interact input sent")

        if debug:
            print("Waiting for screen to turn black")
        
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
        
        if debug:
            print("Screen is black!")

        if debug:
            print("Waiting for save selection to appear (waiting for top screen not to be black)...")

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
        if debug:
            print("Save selection appeared!")

        time.sleep(0.5)
        press_and_release("A")

        if debug:
            print("Interact input sent")

        if debug:
            print("Waiting for screen to turn black")
        
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
        
        if debug:
            print("Screen is black!")