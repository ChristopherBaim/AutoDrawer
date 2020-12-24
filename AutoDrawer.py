import pyautogui
from PIL import Image
from numpy import asarray

# Drawing speed settings
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0.0001  # Set 0 for fastest drawing, 0.0001 or higher if drawing too fast

# Image settings
im = Image.open("assets/source/github.png").convert("L")

pixelSize = 1
colorThreshold = 240

maxDimension = 150
heightAdj = im.height/maxDimension
widthAdj = im.width/maxDimension
adj = max(widthAdj, heightAdj)

imSmall = im.resize((int(im.width/adj),int(im.height/adj)), 4)

imArray = asarray(imSmall)

# Display image properties
def picInfo(picture):
    print("Format: {0}\nSize: {1}\nMode: {2}".format(picture.format,
        picture.size, picture.mode))

# Drawing automation
def drawPixels(data, pxSize, threshold):
    posY = 0
    x, y = pyautogui.position()

    for row in data:
        pyautogui.moveTo(x,y+(posY*pxSize))

        for pixel in row:
            if(pixel<threshold):

                pyautogui.drag(1,0, button='left')
                pyautogui.move(pxSize-1,0)

            else:
                pyautogui.move(pxSize,0)
        posY+=1

drawPixels(imArray, pixelSize, colorThreshold)

# Troubleshooting settings
#im.show() # Show source image
#imSmall.show() # Show scaled image used for drawing
#imSmall.save("ImageOUT", format="PNG") # Save scaled image
