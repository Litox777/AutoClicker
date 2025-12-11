import mouse
import time
import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import pynput
import PIL
from pynput import keyboard

# Variable
running = True
working = False
clickerSpeed = "1"
mousePos = mouse.get_position()

def on_key_release(k):
    if isinstance(k, keyboard.Key):

        if k == keyboard.Key.f5:
            global mousePos
            global posX
            global posY
            mousePos = mouse.get_position()
            posX.set(mousePos[0])
            posY.set(mousePos[1])        

        if k == keyboard.Key.f2:

            global working

            if working == True:
                working = False
                startButton.config(state="active")
                stopButton.config(state="disabled")
            else:
                working = True
                startButton.config(state="disabled")
                stopButton.config(state="active")
listener = keyboard.Listener(on_release = on_key_release)
listener.start()

def startAutoClicker():
    global working
    if working == False:
        working = True
        startButton.config(state="disabled")
        stopButton.config(state="active")

def stopAutoClicker():
    global working
    if working == True:
        working = False
        startButton.config(state="active")
        stopButton.config(state="disabled")

def autoClicker(*args):
    global running
    global working
    global clickerSpeed
    global optionPos

    while running:    
        if working:
            if optionPos.get() == 1:
                if timesTypeVar.get() == "Single":
                    mouse.click(mouseTypeVar.get().lower())

                elif timesTypeVar.get() == "Double":
                    mouse.double_click(mouseTypeVar.get().lower())

                time.sleep(1/clickerSpeed)

            elif optionPos.get() == 0:
                mouse.move(posX.get(), posY.get())
                if timesTypeVar.get() == "Single":
                    mouse.click(mouseTypeVar.get().lower())

                elif timesTypeVar.get() == "Double":
                    mouse.double_click(mouseTypeVar.get().lower())
                
                time.sleep(1/clickerSpeed)
        else: 
            time.sleep(0.1)

def changeValue(*args):
    global working
    global clickerSpeed
    try:
        clickValue = int(textClick.get())
        if clickValue > 0:
            clickerSpeed = clickValue
            print(f"Ha cambiado a: {clickerSpeed}")
    except:
        print(f"Esto {textClick.get()} esta mal")

# Screen
root = tk.Tk()
root.title("Auto Clicker 3000")
root.geometry("460x495")
root.attributes('-topmost', True)
#root.iconbitmap("mouse.ico")
root.resizable(False, False)

# Frame 1 --------------------------------------------------------------------------------------------------

# Clicks per Second
frameRoot = tk.Frame(root)
frameRoot.pack(padx=10, pady=10, fill="both")
frameRoot.columnconfigure(0, weight=1)
frameRoot.columnconfigure(1, weight=1)

frameClick = tk.LabelFrame(frameRoot, text="Clicks per second")
frameClick.grid(row=0, column=0, sticky="w")

textClick = tk.StringVar()
textClick.trace_add(mode='write', callback=changeValue)

cpsEntry = tk.Entry(frameClick,textvariable=textClick)
cpsEntry.pack(pady=20, padx=10)
cpsEntry.insert(0, 1)

# Buttons
frameButtons = tk.Frame(frameRoot) 
frameButtons.grid(row=0, column=1, pady=5   ,padx=10)

startButton = tk.Button(frameButtons, command=startAutoClicker, text="Start AutoClicker")
startButton.pack(pady=5, padx=10)

stopButton = tk.Button(frameButtons, command=stopAutoClicker, text="Stop AutoClicker")
stopButton.pack()
stopButton.configure(state="disabled")

# Frame 2 --------------------------------------------------------------------------------------------------
frameClickOption = tk.LabelFrame(root, text="Click options", padx=10, pady=20)
frameClickOption.pack(padx=10, pady=10, fill="both")
frameClickOption.columnconfigure(0, weight=1)
frameClickOption.columnconfigure(1, weight=1)

textMouseType = tk.Label(frameClickOption,text="Mouse button:")
textMouseType.grid(row=0, column=0, sticky="w")

mouseTypeList = ["Left", "Middle", "Right"]
mouseTypeVar = tk.StringVar()

menuMouseType = ttk.Combobox(frameClickOption, values=mouseTypeList, state="readonly", width=10, textvariable=mouseTypeVar)
menuMouseType.current(0)
menuMouseType.grid(row=0, column=0, sticky="e")


textMouseType = tk.Label(frameClickOption,text="Type of click:")
textMouseType.grid(pady=(15, 3), row=1, column=0, sticky="w")

timesTypeList = ["Single", "Double"]
timesTypeVar = tk.StringVar()

menuTimesType = ttk.Combobox(frameClickOption, values=timesTypeList, state="readonly", width=10, textvariable=timesTypeVar)
menuTimesType.current(0)
menuTimesType.grid(pady=(15, 3), row=1, column=0, sticky="e")



# Frame 3 --------------------------------------------------------------------------------------------------

framePosition = tk.LabelFrame(root, text="Cursor position", padx=10, pady=20)
framePosition.pack(padx=10, pady=10, fill="both")
framePosition.columnconfigure(0, weight=1)
framePosition.columnconfigure(1, weight=1)
framePosition.columnconfigure(2, weight=1)
framePosition.columnconfigure(3, weight=1)

optionPos = tk.IntVar()
optionPos.set(1) 

radioCurrPos = tk.Radiobutton(framePosition, text="Current position", variable=optionPos, value="1")
radioCurrPos.grid(row=1, column=0, sticky="w")
radioCustPos = tk.Radiobutton(framePosition, text="Pick position", variable=optionPos, value="0")
radioCustPos.grid(row=1, column=1, sticky="e")

posX = tk.IntVar()
posY = tk.IntVar()

posxEntry = tk.Entry(framePosition, textvariable=posX, width=6)
posxEntry.grid(row=1, column=2, sticky="e")
posxEntry.insert(0,0)

posyEntry = tk.Entry(framePosition, textvariable=posY, width=6)
posyEntry.grid(row=1, column=3, sticky="e")
posyEntry.insert(0,0)

# Other --------------------------------------------------------------------------------------------------

getPosText = tk.Label(root, text="Press F5 to get position")
getPosText.pack()

startText = tk.Label(root, text="Press F2 to start")
startText.pack()

autoClickerThread = threading.Thread(target=autoClicker)
autoClickerThread.daemon = True
autoClickerThread.start()

root.mainloop()