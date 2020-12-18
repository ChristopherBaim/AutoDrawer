import pyautogui
from PIL import Image
from numpy import asarray

# Drawing speed settings
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0.0001  # Set 0 for fastest drawing, 0.0001 or higher if drawing too fast

# Image settings
im = Image.open("assets/github.png").convert("L")

maxDimension = 75
heightAdj = im.height/maxDimension
widthAdj = im.width/maxDimension
adj = max(widthAdj, heightAdj)

imSmall = im.resize((int(im.width/adj),int(im.height/adj)), 4)

imArray = asarray(imSmall)

# Display image properties
def picInfo(picture):
    print("Format: {0}\nSize: {1}\nMode: {2}".format(picture.format,
        picture.size, picture.mode))

#Drawing automation
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

drawPixels(imArray,4, 100)

# im.show()
# imSmall.show()
# im.save("ImageOUT", format="PNG")
