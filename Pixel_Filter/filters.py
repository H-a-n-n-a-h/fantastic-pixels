import cv2
import numpy as np
from datetime import datetime 

## Saving

# Quick saving with timestamp
def save_with_timestamp(img, name = "filtered"):
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_out_path = name+"_"+time_stamp+".png"
    cv2.imwrite(image_out_path, img)

## Filters

# Simple filters

# Multiplies rgb values globally
def adjust_rgb(input: np.ndarray, red: float, green: float, blue: float) -> np.ndarray:
    size = (input.shape[0], input.shape[1], input.shape[2])
    new_img = np.zeros(size)
    for height in range(size[0]):
        for width in range(size[1]):
            new_img[height, width,0] = blue * input[height, width,0]
            new_img[height, width,1] = green * input[height, width,1]
            new_img[height, width,2] = red * input[height, width,2]
    return new_img


# Blur filters

# given an image and position in that image returns the average color of surrounding neighbors, 
def box_blur_3(img,y,x,border,channel):
    height, width, channels = img.shape

    # pixels at the edge do not have 8 neighbours so we skip them
    if (not (x > border and x < width-border)): return 0
    if (not (y > border and y < height-border)): return 0
    
    # A is a matrix 3x3 containing the pixel at (x,y) position an its surrounding neighbors
    A = np.array(
        [
        [img[y-1][x-1][channel]],[img[y-1][x][channel]], [img[y-1][x][channel]],
        [img[y][x-1][channel]]  ,[img[y][x][channel]]  , [img[y][x+1][channel]],
        [img[y+1][x+1][channel]],[img[y+1][x][channel]], [img[y][x+1][channel]]
        ]
        )
    
    new_pixel_color = A.mean()
    return new_pixel_color

def apply_box_blur_3(new_img,img):
    height, width, channels = img.shape
    # iterate through every pixel
    for y in range(height):
        for x in range (width):
            new_img[y, x] =  [box_blur_3(img,y,x,1,0), box_blur_3(img,y,x,1,1), box_blur_3(img,y,x,1,2)] #applies box blur on all three channels individually
    
    return new_img


# Pixel screen filters

# Scale is how big the window is and dots_size is size of color block, scale - dots_size is grid thickness
def upscale_square_dots(input: np.ndarray, scale: int, dot_size: int) -> np.ndarray:
    size = (input.shape[0]*scale, input.shape[1]*scale, input.shape[2])
    new_img = np.zeros(size)
    for height in range(input.shape[0]):
        for width in range(input.shape[1]):
            for x in range (0,dot_size):
                for y in range (0,dot_size):
                    new_img[scale*height+x, scale*width+y] = input[height, width]
    return new_img

def upscale_nearest_neighbor(input: np.ndarray, scale: int) -> np.ndarray:
    size = (input.shape[0]*scale, input.shape[1]*scale, input.shape[2])
    new_img = np.zeros(size)
    for height_index in range(input.shape[0]):
        for width_index in range(input.shape[1]):
            for x in range (0,scale):
                for y in range (0,scale):
                    new_img[(height_index*scale)+x,(width_index*scale)+y] = input[height_index,width_index]
    return new_img

# Creates and 3x nearest neighbor upscaled image with each 3x3 cell consiting of r, g and b strip
def rgb_effect(input: np.ndarray, scale = 3) -> np.ndarray:
    size = (input.shape[0]*scale, input.shape[1]*scale, input.shape[2])
    new_img = np.zeros(size)
    for height_index in range(input.shape[0]):
        for width_index in range(input.shape[1]):
            for x in range (0,scale):
                for y in range (0,scale):
                    new_img[(height_index*scale)+x,(width_index*scale)+y,y%3] = input[height_index,width_index,y%3]
    new_img = upscale_square_dots(new_img, 4,3)
    return new_img