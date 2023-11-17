#%%
from PIL import Image

def resized_image(image, width, height):
    """
    Resizes the input image to the specified width and height.
    """
    resized_image = image.resize((width, height), Image.LANCZOS)
    return resized_image

def move_center_w_fill(resized_image, width, height):
    """
    Moves the image to the center position and fills in any NaN values with white.
    """
    
    # Create a new blank image with the desired dimensions
    new_image = Image.new('RGB', (width, height), (255, 255, 255))
    
    # Calculate the position to paste the resized image
    x_offset = (width - resized_image.width) // 2
    y_offset = (height - resized_image.height) // 2
    
    # Paste the resized image onto the new image at the calculated position
    new_image.paste(resized_image, (x_offset, y_offset))
    
    return new_image
#%%
def main(path_to_your_image, path_to_save_image, new_length = 500):
    # Resize to squere and center-fill the image to a specific width and height
    original_image = Image.open(path_to_your_image)

    if original_image.width < original_image.height:
        height = new_length
        width = int(original_image.width * new_length / original_image.height)
    else:    
        height = int(original_image.height * new_length / original_image.width)
        width = new_length

    print(f"o_height:{original_image.height}, o_width:{original_image.width}")
    print(f"height:{height}, width:{width}")
    # %%
    image_of_converted = resized_image(original_image, 640, 320)
    center_filled_image = move_center_w_fill(image_of_converted, new_length, new_length)

    # Save the resulting image to a file
    center_filled_image.save(path_to_save_image)  # Replace with the desired output path


# %%
if __name__ == '__main__':
    # Example usage
    import argparse
    parser = argparse.ArgumentParser(description='Convert image')
    parser.add_argument('--path_origin', '-p', type=str, help='original image path')
    parser.add_argument('--out_path', '-o', type=str, help='output image path')
    parser.add_argument('--new_length', '-l', type=int, help='The length of one side of the new image')
    args = parser.parse_args()
    # print(f"path_to_your_image:{args.path_origin}")
    # print(f"path_to_save_image:{args.out_path}")
    main( args.path_origin, args.out_path, args.new_length )
