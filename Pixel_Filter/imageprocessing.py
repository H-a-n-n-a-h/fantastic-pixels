
import numpy as np
import cv2

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


path = "sample.png"
img = cv2.imread(path)
new_img = np.zeros(img.shape)
apply_box_blur_3(new_img, img)

cv2.imwrite('filtered_'+path, new_img, [cv2.IMWRITE_PNG_COMPRESSION, 0])

