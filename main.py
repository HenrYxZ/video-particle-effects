import numpy as np
from PIL import Image

# Local Modules
import fast
import utils

TEST_IMAGE = "images/sigur_ros.jpg"
MAX_INTENSITY = 255
OUTPUT_FILENAME = "output/fast_slow.jpg"
MAX_QUALITY = 95


def open_image(img_filename):
    img = Image.open(img_filename)
    img_array = np.array(img)
    return img_array


def draw_red_dots(img_arr, features):
    h, w, channels = img_arr.shape
    for j in range(h):
        for i in range(w):
            if (j, i) in features:
                img_arr[j][i] = (MAX_INTENSITY, 0, 0)


def main():
    print("Processing...")
    timer = utils.Timer()
    timer.start()
    img_arr = open_image(TEST_IMAGE)
    output = np.zeros(img_arr.shape, dtype=np.uint8)
    features = fast.detect(img_arr)
    draw_red_dots(output, features)
    output_img = Image.fromarray(output)
    output_img.save(OUTPUT_FILENAME, quality=MAX_QUALITY)
    timer.stop()
    print(f"Total time spent {timer}")


if __name__ == '__main__':
    main()
