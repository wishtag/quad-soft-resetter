import os
from PIL import ImageGrab
import pyautogui
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
windows = [[[664,94,957,270], [664,272,957,492], [1,94,664,492]], [[1624,94,1917,270], [1624,272,1917,492], [961,94,1624,492]], [[664,607,957,783], [664,785,957,1005], [1,607,664,1005]], [[1624,607,1917,783], [1624,785,1917,1005], [961,607,1624,1005]]]

instances_status = [False,False,False,False]

debug = True
save_encounters = True
json_time = read_json("resets.json")["total_seconds"]
delays = [0,0,0,0]
encounters = [0,0,0,0]
is_shiny = False
name = "Pheromosa"
webhook_url = ""
webhook_url_enc = ""
game = "Ultra Moon"
game_id = "00040000001B5100"

hour = datetime.now(timezone('US/Central')).hour
minute = datetime.now(timezone('US/Central')).minute
second = datetime.now(timezone('US/Central')).second
start_time = (hour*60**2) + (minute*60) + second

try:
    os.remove('img/screenshot.png')
except:
    pass

clear_screen()
temp = read_json("resets.json")["last_delays"]
print(f"Would you like to reset {Fore.GREEN}[last_delays]{Style.RESET_ALL}? Current values are: {Fore.GREEN}{temp}{Style.RESET_ALL}")
choice = input("[y/n]: ")
if choice == "y" or choice == "Y":
    resets = read_json("resets.json")
    resets["last_delays"] = [0,0,0,0]
    write_json("resets.json", resets)


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
    
    if save_encounters:
        try:
            os.remove('img/screenshot0.png')
        except:
            pass
        try:
            os.remove('img/screenshot1.png')
        except:
            pass
        try:
            os.remove('img/screenshot2.png')
        except:
            pass
        try:
            os.remove('img/screenshot3.png')
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
    press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

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
    resets = read_json("resets.json")
    resets["resets"] = resets["resets"] + 4
    resets["total_seconds"] = json_time + elapsed_time
    write_json("resets.json", resets)

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
                    if save_encounters == True:
                        encounters[i].save(f"img/screenshot{i}.png")
                screenshot = ImageGrab.grab(bbox=windows[i][0])
                pixels = screenshot.load()
                screenshot.close()

                r, g, b = pixels[4, 135]
                if r == 255 and g == 68 and b == 34:
                    instances_status[i] = True
    instances_status = [False,False,False,False]
    
    if debug:
        print("Encounter introduction ended!")

    if debug and save_encounters:
        print("Creating save states...")
        resets = read_json("resets.json")

        seconds = resets["total_seconds"]

        in_minutes = seconds / 60

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        time_formatted = f"{hours} hours, {minutes} minutes, and {seconds} seconds"

        for i in range(4):
            try:
                os.remove(sorted(os.scandir("C:/Users/myname/AppData/Roaming/Citra/states"), key=lambda entry: entry.stat().st_mtime, reverse=True)[0].path)
            except:
                pass
            coords = []
            if i == 0:
                coords = [495, 270]
            elif i == 1:
                coords = [1485, 270]
            elif i == 2:
                coords = [495, 810]
            elif i == 3:
                coords = [1485, 810]
            
            made_save_state = False
            while made_save_state == False:
                pyautogui.click(coords)
                time.sleep(.1)
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(1)
                screenshot = ImageGrab.grab(bbox=(0,0,1920,1080))
                pixels = screenshot.load()
                screenshot.close()

                r, g, b = pixels[781, 521]
                if r != 252 or g != 225 or b != 0:
                    made_save_state = True
                    print("no error")
                else:
                    if i != 0:
                        pyautogui.click(890, 470)
                        time.sleep(0.1)
                    pyautogui.click(1089, 553)
                    time.sleep(0.5)

            webhook = DiscordWebhook(url=webhook_url_enc, username="Sparkles")
            with open(f"img/screenshot{i}.png", "rb") as f:
                webhook.add_file(file=f.read(), filename="screenshot.png")
            with open(sorted(os.scandir("C:/Users/myname/AppData/Roaming/Citra/states"), key=lambda entry: entry.stat().st_mtime, reverse=True)[0].path, "rb") as f:
                webhook.add_file(file=f.read(), filename=f"{game_id}.0{i+1}.cst")
            embed = DiscordEmbed(title=f"{name} Found", description=f"Encounter {int(resets['resets'])-(4-(i+1))}, on instance {i+1}, over the span of {time_formatted}", color="E5D6C7")
            embed.set_author(name=f"{name} Encounter Logged", icon_url="https://cdn.discordapp.com/attachments/711024686690992240/1294018023228837969/sparkel.png?ex=67097bb2&is=67082a32&hm=8cbe9833e828267a6df37035066318e910691279108ee50f82176e26d3ab81e2&",)
            embed.set_image(url="attachment://screenshot.png")
            embed.add_embed_field(name="Total Time in Minutes", value=str(in_minutes))
            embed.set_footer(text=game)
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()

    if debug:
        print("Comparing delays...")

    resets = read_json("resets.json")
    for i in range(len(resets["last_delays"])):
        if resets["last_delays"][i] == 0:
            resets["last_delays"][i] = delays[i]
    write_json("resets.json", resets)
    

    avg = (delays[0]+delays[1]+delays[2]+delays[3])/4
    for i in range(4):
        if abs(avg-delays[i]) < 3:
            instances_status[i] = True

    resets = read_json("resets.json")
    for i in range(len(resets["last_delays"])):
        print(abs(resets["last_delays"][i]-delays[i]))
        if abs(resets["last_delays"][i]-delays[i]) > 8:
            if not_ready(instances_status):
                encounters[i].save("img/screenshot.png")
                for i in range(4):
                    try:
                        encounters[i].close()
                    except:
                        pass

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
                embed = DiscordEmbed(title=f"Shiny {name} Found", description=f"{resets['resets']} resets over the span of {time_formatted} on instance {i+1}", color="FCDE3A")
                embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
                embed.set_image(url="attachment://screenshot.png")
                embed.add_embed_field(name="Total Time in Minutes", value=str(in_minutes))
                embed.set_footer(text=game)
                embed.set_timestamp()
                webhook.add_embed(embed)
                response = webhook.execute()

                resets["last_delays"] = delays
                write_json("resets.json", resets)
    if is_shiny == False:
        #webhook = DiscordWebhook(url=webhook_url, username="Sparkles")
        #embed = DiscordEmbed(title=f"Not Shiny", description="Placeholder", color="FCDE3A")
        #embed.set_author(name="Shiny Found", icon_url="https://em-content.zobj.net/source/apple/391/sparkles_2728.png",)
        #webhook.add_embed(embed)
        #webhook.execute()

        instances_status = [False,False,False,False]

        if debug:
            print("Normal encounter delay")
            print("Softresetting...")

        resets = read_json("resets.json")
        resets["last_delays"] = delays
        write_json("resets.json", resets)

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
        press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

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
        press_and_release(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)

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