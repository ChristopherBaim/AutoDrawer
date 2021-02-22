## Auto Drawer
Auto Drawer is a simple freehand drawing application using mouse automation.
From a source image, it draws a [binary image](https://en.wikipedia.org/wiki/Binary_image)
in applications that allow freehand mouse drawing (ex. Microsoft Paint or [Roll20](https://roll20.net/)).

<p align="center">
  <img src="/assets/examples/OctocatGIF.gif" width="500">
  <br>
  <b>GitHub logo drawn with Auto Drawer</b>
</p>


## Motivation
Online gaming services, like Roll20, often allow users to freehand draw onto maps 
for other players to see. I wanted a way to make decent drawings without requiring
a drawing tablet and artistic skill. 

## Features
Works with any common image file format (ex. PNG, JPEG, BMP, GIF, TIFF)

Adjustable drawing settings including resolution, size, and speed

| <img src="/assets/source/github.jpg" height="100"> | <img src="/assets/examples/Resolution.png" height="100"> | <img src="/assets/examples/Scales.png" height="100"> | <img src="/assets/examples/GithubCrop.gif" height="100"> |
| :---: | :---: | :---: | :---: |
| *Source* | *Resolution* | *Size* | *Speed* |

## Examples

#### Works with photographs

| <img src="/assets/source/face.jpg" height="200"> | <img src="/assets/examples/FaceDrawn.png" height="200"> | <img src="/assets/examples/FaceDrawnHighRes.png" height="200"> |
| :---: | :---: | :---: |
| *Source* | *Low Resolution* | *High Resolution* |

#### Works with color images

| <img src="/assets/source/GreatWave.jpg" height="200"> | <img src="/assets/examples/GreatWaveDrawn.png" height="200"> | 
| :---: | :---: |
| *Source* | *Output* | 

## Built using
- [Pillow (PIL Fork)](https://pillow.readthedocs.io/en/stable/#) for image processing
- [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) for mouse automation
- [NumPy](https://numpy.org/) to organize image data array
