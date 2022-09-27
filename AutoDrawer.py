from tkinter import *
from tkinter import filedialog
from PIL import ImageTk,Image, ImageOps
import pyautogui
from numpy import asarray
import keyboard

class Picture(object):
    def __init__(self):
        self.source = Image.new(mode="RGB", size = (0,0))
        self.source_preview = Image.new(mode="RGB", size = (0,0))
        self.thresh_preview = Image.new(mode="RGB", size = (0,0))

class Settings(object):
    def __init__(self):
        self.RGB = None
        self.size = None
        self.resolution = None
        self.armed = False
        self.threshold = None
        self.interrupted = False

def loadPic():
    global img

    # Load image and adjust size to fit window
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files", "*.*"), ("jpeg files","*.jpg")))
    pic.source = Image.open(filename).convert("RGB")

    adj = max(pic.source.width, pic.source.height) / 250
    wAdj = int(pic.source.width / adj)
    hAdj = int(pic.source.height / adj)
    settings.size = (wAdj, hAdj)

    pic.source_preview = pic.source.resize((wAdj, hAdj), 4)
    img = ImageTk.PhotoImage(pic.source_preview)

    # Configure frame column widths
    for x in range(0,4):
        topFrame.columnconfigure(x,weight=1)
        midFrame.columnconfigure(x, weight=1, minsize=125)
        botFrame.columnconfigure(x, weight=1, minsize=125)

    # topFrame layout
    topFrame.grid_propagate(0)
    topFrame.config(width=500, height=45)
    load.config(text='Replace Image')

    load.grid(column=1, columnspan=2)

    l1.place(x=-30+pic.source_preview.width/2, y=20)
    l2.place(x=465-(pic.source_preview.width/2), y=20)

    # canvas layout
    canvas.config(width = 500, height=int(pic.source.height / adj))
    canvas.pack()
    canvas.delete("source")
    canvas.create_image(0, 0, anchor=NW, image=img, tag="source")

    # midFrame layout
    midFrame.grid_propagate(0)
    midFrame.config(width=500, height=115)
    Label(midFrame, text="Image Settings", font='bold').grid(row=0, column=1, columnspan=2)

    Label(midFrame, text="Channel").grid(row=1, column=0)
    w1.grid(row=2, column=0)

    Label(midFrame, text="Threshold").grid(row=1, column=1)
    w2.grid(row=2, column=1)
    w2.set(125)

    Label(midFrame, text="Resolution").grid(row=1, column=2)
    w3.grid(row=2, column=2)
    w3.set(100)

    Button(midFrame, text='Invert Image', command=lambda: invertPreview()).grid(row=2, column=3)

    # botFrame layout
    botFrame.grid_propagate(0)
    botFrame.config(width=500, height=135)
    Label(botFrame, text="Drawing Settings", font='bold').grid(row=0, column=1, columnspan=2)

    Label(botFrame, text="Image Size").grid(row=1, column=0)
    Label(botFrame, text="W:").grid(row=2, column=0, sticky=W, padx=33)
    Label(botFrame, text="H:").grid(row=3, column=0, sticky=W, padx=35)
    sizeW.grid(row=2, column=0, sticky=E, padx=(0,35))
    sizeH.grid(row=3, column=0, sticky=E, padx=(0,35))
    sizeW.delete(0, "end")
    sizeW.insert(END, wAdj)
    sizeH.delete(0, "end")
    sizeH.insert(END, hAdj)
    sizeSet.grid(row=4, column=0, sticky=W, padx=25, pady=4)
    sizeReset.grid(row=4, column=0, sticky=E, padx=(0,20), pady=4)

    Label(botFrame, text="Pixel Size").grid(row=1, column=1)
    pxSize.grid(row=2, column=1)
    pxSize.delete(0, "end")
    pxSize.insert(END, 1)
    Label(botFrame, text="Speed").grid(row=1, column=2, padx=20 )
    speedSet.grid(row=2, column=2)

    arm.grid(row=2, column=3)

    # Generate initial preview with default settings
    show_values(None)

def show_values(event):
    global img2

    imSmall = pic.source_preview
    settings.threshold = w2.get()
    settings.resolution = w3.get()

    # Adjust image resolution
    if settings.resolution < 100:
        width, height = pic.source_preview.size
        smallWidth = int(width * (settings.resolution / 100))
        smallHeight = int(height * (settings.resolution / 100))

        lowRes = pic.source_preview.resize((smallWidth, smallHeight))
        imSmall = lowRes.resize((width, height), 4)

    # Threshold image
    if RGBvar.get() == "All":
        im2 = imSmall.convert('L').point(lambda p: p > settings.threshold and 255)
    else:
        if RGBvar.get() == "Red":
            settings.RGB = 0
        elif RGBvar.get() == "Green":
            settings.RGB = 1
        elif RGBvar.get() == "Blue":
            settings.RGB = 2

        rgb = imSmall.split()
        im2 = rgb[settings.RGB].point(lambda p: p > settings.threshold and 255)

    pic.thresh_preview = im2
    img2 = ImageTk.PhotoImage(im2)

    canvas.delete("preview")
    canvas.create_image(500-im2.width, 0, anchor=NW, image=img2, tag="preview")

def updateSize():

    width = sizeW_var.get()
    height = sizeH_var.get()

    if width != settings.size[0] and height != settings.size[1]:
        settings.size = (width, height)
    elif width != settings.size[0]:
        adj = settings.size[0] / width
        height = int(settings.size[1] / adj)
        settings.size = (width, height)

        sizeH.delete(0, "end")
        sizeH.insert(END, height)
    elif height != settings.size[1]:
        height = sizeH_var.get()
        adj = settings.size[1] / height
        width = int(settings.size[0] / adj)
        settings.size = (width, height)

        sizeW.delete(0, "end")
        sizeW.insert(END, width)

def resetSize():

    width, height = pic.source_preview.size
    settings.size = (width, height)

    sizeW.delete(0, "end")
    sizeW.insert(END, width)
    sizeH.delete(0, "end")
    sizeH.insert(END, height)

def setSpeed(speed):
    # Set seconds to pause between each mouse movement
    if speed == "Fastest":
        pyautogui.PAUSE = 0
    elif speed == "Fast":
        pyautogui.PAUSE = 0.001
    elif speed == "Medium":
        pyautogui.PAUSE = 0.015
    elif speed == "Slow":
        pyautogui.PAUSE = 0.05

def armDrawing():

    if settings.armed:
        arm.config(relief="raised", text=" Arm ", fg="black")
    else:
        arm.config(relief="sunken", text="Armed", fg="red")

    settings.armed = not settings.armed

def moveMouse(event):
    settings.interrupted = False
    im2 = pic.thresh_preview.resize(settings.size, 1)
    im2= im2.convert('L').point(lambda p: p > settings.threshold and 255)

    pxSize = pxSize_var.get()

    # Draw image with mouse automation
    if settings.armed:
        data = asarray(im2)
        posY = 0
        x, y = pyautogui.position()

        for row in data:
            if settings.interrupted == True:
                break
            pyautogui.moveTo(x, y + (posY * pxSize))
            current = row[0]
            run = 0
            for pxNum in range(0,len(row)):
                if row[pxNum] == current:
                    run += 1
                    if pxNum == len(row)-1:
                        if current == 0:
                            pyautogui.drag(run * pxSize, 0, button='left')
                            run = 1
                            current = 255
                        else:
                            pyautogui.move(run * pxSize, 0)
                            run = 1
                            current = 0
                else:
                    if current == 0:
                        pyautogui.drag(run * pxSize, 0, button='left')
                        run = 1
                        current = 255
                    else:
                        pyautogui.move(run * pxSize, 0)
                        run = 1
                        current = 0
            posY += 1

    # Move mouse to preview final size of drawing
    else:
        pyautogui.move(settings.size[0]*pxSize, settings.size[1]*pxSize, 0.5)
        print(settings.size[0],settings.size[1])

def invertPreview():

    pic.source_preview = ImageOps.invert(pic.source_preview)
    w2.set(abs(255 - w2.get()))
    show_values(None)

def interrupt():
    print("Killed")
    settings.interrupted = True


pic = Picture()
settings = Settings()

pyautogui.PAUSE = 0.001

root = Tk()
root.title('Auto Drawer')

# Define tkinter frames
topFrame = Frame(root)
topFrame.grid()
topFrame.grid_propagate(0)
topFrame.config(width=220, height=50)
topFrame.grid_columnconfigure(0, weight=1)
topFrame.grid_rowconfigure(0, weight=1)
canvasFrame = Frame(root)
canvasFrame.grid()
midFrame = Frame(root, border=2, relief='raised')
midFrame.grid()
botFrame = Frame(root, border=2, relief='raised')
botFrame.grid()

# Create input variables
RGBvar = StringVar()
sizeH_var = IntVar()
sizeW_var = IntVar()
pxSize_var = IntVar()
speed_var = StringVar()

# Start listening for keyboard input
root.bind('<Return>', lambda event: moveMouse(event))
root.focus_force()
interrupted = False
keyboard.add_hotkey("esc", lambda: interrupt())

# Create widgets for each frame
load = Button(topFrame, text='Load Image', command=loadPic)
load.grid()
l1 = Label(topFrame, text="Source", font='bold')
l2 = Label(topFrame, text="Preview", font='bold')

canvas = Canvas(canvasFrame, width=500, height=100)

w1 = OptionMenu(midFrame, RGBvar, "All", "Red", "Green", "Blue", command=show_values)
RGBvar.set("All")
w2 = Scale(midFrame, from_=0, to=255, length=100, tickinterval=125, orient=HORIZONTAL, command=show_values)
w3 = Scale(midFrame, from_=1, to=100, length=100, tickinterval=99, orient=HORIZONTAL, command=show_values)

sizeW = Entry(botFrame, width=5, textvariable=sizeW_var)
sizeH = Entry(botFrame, width=5, textvariable=sizeH_var)
sizeSet = Button(botFrame, text="Enter", command=updateSize)
sizeReset = Button(botFrame, text="Reset", command=resetSize)
speedSet = OptionMenu(botFrame, speed_var,"Fastest","Fast","Medium","Slow", command=setSpeed)
speed_var.set("Fast")
pxSize = Entry(botFrame, width=5, textvariable=pxSize_var)
arm = Button(botFrame, text=" Arm ", command=armDrawing)


mainloop()