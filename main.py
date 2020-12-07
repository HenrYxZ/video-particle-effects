import imageio
import numpy as np
import os.path
from PIL import Image
from progress.bar import Bar
import cv2 as cv

# Local Modules
from effects import particle_effects
# import fast
from render import render
import utils

VIDEOS_DIR = "videos"
TEST_IMAGE = "images/sigur_ros.jpg"
MAX_INTENSITY = 255
OUTPUT_FILENAME = "output/fast.jpg"
VIDEO_FILENAME = f"{VIDEOS_DIR}/explosions.mp4"
OUT_VIDEO_FILENAME = f"{VIDEOS_DIR}/out.mp4"
MAX_QUALITY = 95
THRESHOLD = 50
# duration of video in seconds
DURATION = 6 * 60 + 29
FPS = 29.970030


def draw_red_dots(img_arr, features):
    for feature in features:
        i = int(round(feature[0]))
        j = int(round(feature[1]))
        img_arr[j][i] = (MAX_INTENSITY, 0, 0)


def process_keypoints(kp):
    """
    Get keypoints as 2D ndarray
    Args:
        kp([Keypoint]):
    Returns:
         ndarray: list of 2D ndarray that represent the key points
    """
    keypoints = [x.pt for x in kp]
    return keypoints


def main():
    # Initiate FAST object with default values
    fast = cv.FastFeatureDetector_create(threshold=THRESHOLD)
    print("Processing...")
    timer = utils.Timer()
    timer.start()
    # Create frames from video
    # reader = imageio.get_reader(f'imageio:videos/explosions.mp4')
    # for i, img in enumerate(reader):
    # For creating video
    if not os.path.exists(VIDEOS_DIR):
        os.mkdir(VIDEOS_DIR)
    writer = imageio.get_writer(OUT_VIDEO_FILENAME, fps=FPS)
    print(f"Getting keypoints from video {VIDEO_FILENAME}...")
    # Reading video
    cap = cv.VideoCapture(VIDEO_FILENAME)
    counter = 0
    total_frames = DURATION * FPS
    step_size = np.ceil(total_frames / 100).astype(int)
    bar = Bar("Processing...", max=100, suffix='%(percent)d%%')
    bar.check_tty = False
    particles = []
    h = None
    w = None
    while cap.isOpened():
        ret, frame = cap.read()
        if not h:
            w, h, _ = frame.shape
        kp = fast.detect(frame, None)
        # Get list of keypoints per frame
        keypoints = process_keypoints(kp)
        # Apply effect to keypoints (create particles per frame)
        delta_time = 1 / FPS
        particles = particle_effects(keypoints, particles, delta_time, w, h)
        # Render the particles into an image for the output video
        img_arr = render(particles)
        # Append rendered image into video
        writer.append_data(img_arr)
        # Write rendered image into image file
        if counter < 90:
            img = Image.fromarray(img_arr)
            output_img_filename = f"output/{counter}.jpg"
            img.save(output_img_filename, quality=MAX_QUALITY)
        counter += 1
        if counter % step_size == 0:
            bar.next()
        # Check if this is the end of the video
        if not ret:
            break
    cap.release()
    bar.finish()
    print("Writing video")
    writer.close()
    timer.stop()
    print(f"Total time spent {timer}")


def test():
    timer = utils.Timer()
    timer.start()
    img = cv.imread(TEST_IMAGE, 0)
    fast = cv.FastFeatureDetector_create(threshold=THRESHOLD)
    kp = fast.detect(img, None)
    keypoints = process_keypoints(kp)
    img_arr = np.zeros([720, 1280, 3], dtype=np.uint8)
    draw_red_dots(img_arr, keypoints)
    img = Image.fromarray(img_arr)
    img.save("test.jpg", quality=MAX_QUALITY)
    timer.stop()
    print(f"Total time spent {timer}")


if __name__ == '__main__':
    main()
