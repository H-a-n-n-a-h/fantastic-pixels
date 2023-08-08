import cv2
import numpy as np
from datetime import datetime 

#meta data about image
time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
image_path = "platinum.png"
image_name = f"{image_path[0:len(image_path)-4]}_{time_stamp}.png"
image_array = cv2.imread(image_path)


def adjust_rgb(input: np.ndarray, red: float, green: float, blue: float) -> np.ndarray:
    size = (input.shape[0], input.shape[1], input.shape[2])
    new_img = np.zeros(size)
    for height in range(size[0]):
        for width in range(size[1]):
            new_img[height, width,0] = blue * input[height, width,0]
            new_img[height, width,1] = green * input[height, width,1]
            new_img[height, width,2] = red * input[height, width,2]
    return new_img

def upscale_dots(input: np.ndarray, scale: int, dot_size: int) -> np.ndarray:
    size = (input.shape[0]*scale, input.shape[1]*scale, input.shape[2])
    new_img = np.zeros(size)
    for height in range(input.shape[0]):
        for width in range(input.shape[1]):
            for x in range (0,dot_size):
                for y in range (0,dot_size):
                    new_img[scale*height+x, scale*width+y] = input[height, width]

           # new_img[scale*height, scale*width] = input[height, width]
            #new_img[scale*height+1, scale*width] = input[height, width]
            #new_img[scale*height, scale*width+1] = input[height, width]
            #new_img[scale*height+1, scale*width+1] = input[height, width]
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

#creates and 3x nearest neighbor upscaled image with each 3x3 cell consiting of r, g and b strip
def rgb_effect(input: np.ndarray, scale = 3) -> np.ndarray:
    size = (input.shape[0]*scale, input.shape[1]*scale, input.shape[2])
    new_img = np.zeros(size)
    for height_index in range(input.shape[0]):
        for width_index in range(input.shape[1]):
            for x in range (0,scale):
                for y in range (0,scale):
                    new_img[(height_index*scale)+x,(width_index*scale)+y,y%3] = input[height_index,width_index,y%3]
    new_img = upscale_dots(new_img, 4,3)
    return new_img


#new_modified_image = upscale_nearest_neighbor(image_array, 32)
new_modified_image = rgb_effect(adjust_rgb(image_array,2,2,2), 3)
#new_modified_image = adjust_rgb(image_array, new_image_size, 3,1,1)
#new_modified_image = upscale_dots(image_array, 10)
#print(new_image_size)
#new_image = np.zeros(image_array.shape)
cv2.imwrite(image_name, new_modified_image)
#cv2.imwrite(image_name, new_image)
#cv2.imwrite(image_name, image_array)