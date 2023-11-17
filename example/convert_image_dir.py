from convert_image import main as convert_image_main

import os
import glob
import glob

def get_image_paths(directory_path, image_extensions=['.jpg', '.jpeg', '.png']):
    image_paths = []
    for extension in image_extensions:
        pattern = os.path.join(directory_path, '**', '*' + extension)
        image_paths.extend(glob.glob(pattern, recursive=True))
    return image_paths


if __name__ == "__main__":
    
    # Replace 'your_directory_path' with the actual directory you want to search in
    # directory_path = 'your_directory_path'
    # new_length = 500
    import argparse
    parser = argparse.ArgumentParser(description='Convert image')
    parser.add_argument('--directory_path', '-p', type=str, help='original image dir')
    parser.add_argument('--new_length', '-l', type=int, help='The length of one side of the new image')
    args = parser.parse_args()

    image_paths = get_image_paths(args.directory_path)
    [convert_image_main(path, path, args.new_length) for path in image_paths]
