# Quad Soft Resetter
A python program for Ultra Sun and Ultra Moon playing on Citra that soft resets on 4 instances until it finds a shiny  

This is a project I was really proud of at the time, but this is not something I'd recommend you use.
# Features
## Multi Instance Soft Resetting
Through the `vgamepad` library, the program is able to send inputs to the game. Gamepad inputs are registered by Citra even if you don't have the window focussed so you are able to control multiple instances at once through only one gamepad.  
## Logging
Tracks and saves the total encounters and elapsed time to `resets.json`.  
## Shiny Detection
In USUM, shiny pokémon have a special animation that plays when they are encountered. This animation delays the appearance of the UI. The program tracks the delays across all 4 instances and then compares them. If one is different enough from the others, then it is likely a shiny and the program recognizes it as such.  
## Discord Notifying
Through the use of a discord webhook, the program will notify you when it finds a shiny.  
# Showcase
Here's a little video showing off the program in action  
https://github.com/user-attachments/assets/d6663d3b-735d-49d8-b5c1-8967a6ddba2b
# Setup
I designed this program with a specific window position, size, and resolution. So if you're set up isn't the exact same as mine, then you probably shouldn't use this program.  

If your display isn't 1080p then you're out of luck. If it is, open 4 instances of Citra and position one in each corner. The `Screen Layout` should be set to `Hybrid` and `Show Status Bar` should be enabled. Your `Texture Filter` should also be set to `MMPX`. This should be all you have to do.  
# Usage
## `register_gamepad.py`
This is just a simple python script used to help setup controls. Go to the controls section in Citra and create a new profile, the name doesn't matter. Click the "Auto Map" button and then start the python script. The python script will start counting down, before it finishes click the "OK" button on the popup from Citra. If everything worked correctly, the controller should be mapped.  
## `mash_through_title.py`
As the name suggests, this python script just mashes through the title screen on all instances.  
## `soft_reset_all_instances.py`
I really don't think I need to explain the name for this one, just read the name.  
## `main.py`
This is where everything really goes down. If you've successfully setup everything else then you just have to let this program run. Once it finds a shiny you'll be notified. This also logs the encounters and time spent to `resets.json`.