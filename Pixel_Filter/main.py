from filters import*

#meta data about image
time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
image_in_path = "source/"
image_in_name = "stahh.png"

image_out_path = "output/"
image_out_name = f"{image_out_path}{image_in_name[0:len(image_in_name)-4]}_{time_stamp}.png"
image_array = cv2.imread(f"{image_in_path}{image_in_name}")

new_modified_image = rgb_effect(adjust_rgb(image_array,2,2,2), 3)
cv2.imwrite(image_out_name, new_modified_image)

#ignore this 
'''
new_modified_image = upscale_nearest_neighbor(image_array, 32)
new_modified_image = rgb_effect(adjust_rgb(image_array,2,2,2), 3)
new_modified_image = adjust_rgb(image_array, new_image_size, 3,1,1)
new_modified_image = upscale_dots(image_array, 10)
print(new_image_size)
new_image = np.zeros(image_array.shape)
cv2.imwrite(image_name, new_modified_image)
cv2.imwrite(image_name, new_image)
cv2.imwrite(image_name, image_array)
'''