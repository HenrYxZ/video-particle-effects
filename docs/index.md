# 2D Feature Particles

By Jesús Henríquez

An open source Python app that creates 2D particles from images (or videos
) using feature points from Computer Vision feature detectors. Giving the
information of the silhouettes in some cool abstract open to interpretation 
way.

## Final Report - Dec 4, 2020

### Problem

I wanted to recreate a video effect that I saw in a concert where the images are
replaced by black backgrounds and red points that go around the silhouettes,
suggesting the shapes.

### Previous Work

In a quick search in Google I couldn't find a video effect like that, so I 
had to figure out myself how to do it.

In Computer Vision there are automatic ways to get keypoints from an image 
(they are used to describe images). I had the idea of using the position of
these keypoints to generate the red dots. The FAST corner detector is one that
calculates very quick so I chose to use that. I use OpenCV for that
[https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_fast/py_fast.html](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_fast/py_fast.html)

I also use Particles that can have certain life span, color and movement.

I use this Python libraries:
- imageio - for creating a video output
- opencv-python - to get FAST corner keypoints from images
- pillow - for saving images
- progress - to show a progress bar with the percent done in the program as 
  it runs
- numpy - to use arrays

### My work

I downloaded a live concert from Youtube of my favorite band to work on it.
[https://www.youtube.com/watch?v=zNaUv_XYFGg](https://www.youtube.com/watch?v=zNaUv_XYFGg)

Made the code to read the video frame by frame, getting keypoints for each one,
and creating a new particle for each keypoint, then render the current particles
into an output frame and appending them, and finally create the video with the
set of output frames.

```python
ret, frame = cap.read()
kp = fast.detect(frame, None)
# Get list of keypoints per frame
keypoints = process_keypoints(kp)
# Apply effect to keypoints (create particles per frame)
particles = particle_effects(keypoints, [])
# Render the particles into an image for the output video
img_arr = render(particles)
# Append rendered image into video
writer.append_data(img_arr)
```


### Results

Creating particles that are only alive for one frame it takes less than 3 
minutes to process the 6 min 30 sec video in an AMD Ryzen 4900HS 8-core 
processor.

[output video]('out.mp4')

And using particles that are alive for 1.25 seconds is this, it takes almost
15 min to compute.

[output video]('delay.mp4')

### Analysis

One main issue with FAST feature is they are depending on a threshold parameter,
so you have to try many threshold values to find one that gives good results.

Is also a big difference in computing time when more particles are added per
frame. The entire video has about 12000 frames.

Finally, I think the results are good, they give a stylistic view that is open
to interpretation of the listener and invites him to wonder. But sometimes the
randomness of the features might distract the viewer if it is not very clear
what is in the screen or if it is too noisy.

### Future work

I implemented rigid body physics for the Particles, but I didn't have enough
time to apply it, so in the future one could apply a force that would move the
particles in time. The same with color and scale of the particles. Here is an
example of how it can be done:

```python
# Only use the particles that are alive
particles = list(
    filter(lambda elem: elem.is_alive(current_time), particles)
)

for particle in particles:
    percent = (current_time - particle.creation_time) / particle.life_span
    # Fade out in time
    particle.color *= (1 - percent)
    # Decrease size in time
    particle.rigid_body.state.transform.scale = 1 - percent
    # move by force
    f = np.array([1, 1])
    particle.rigid_body.state = particle.rigid_body.next_state(delta_time, f)
```

## Project Update - Nov 20, 2020

I knew I could use OpenCV for getting FAST features, but I didn't have it
installed in my computer and haven't used it for about 4 years, so I looked
again at how to implement FAST features to do it myself without OpenCV.

It was a bit difficult so I looked for an implementation in Python online and 
found this [https://github.com/tbliu/FAST](https://github.com/tbliu/FAST).

I tried it and had this result:

![original](sigur_ros.jpg)
Original Image  

![fast slow](fast_slow.jpg)
Result Using FAST from tbliu (It looks good but I think it would be better if
the points are not so close from each other, I might have to do something to
sample them spatially)

But the time to generate it was far from "FAST". It took 1 minute to generate
one image, so clearly is not for real-time (like what I saw in the concert) but
anyway I wasn't expecting to make it work in real-time, my goal is to generate
a video offline with a duration of at least a minute. At 30 FPS that would be
generating 1800 images. That would make 1800 minutes or 30 hours of processing.

That's a lot of hours, but I should be able to run it remotely in the lab
from the university (I have successfully run other Python programs for days
before). But that is not counting the particles part of the program, all the
physics calculations...

I think the calculations shouldn't take too much time per frame and I should be
able to implement them somewhat efficiently, so that doesn't worry me much. I
would not be implementing collision detection, the particles would just have
lifespan, position, velocity and color.

I think also the fact that I'm using a HD image adds complexity to the feature
detection part. There are millions of pixels that have to be checked, and I
wouldn't use smaller images because that would eliminate image quality that I
think it's important for the aesthetics in this case.

Finally, I installed OpenCV in a Ubuntu WLS inside Windows, and I will be trying
to use that instead. I didn't have enough time to create the particle class, so
I will also work on that next.

### Summary

- I got a working test of FAST feature detection. It's too slow and points are
 too close from each other.
- I installed OpenCV, I'll try their implementation.
- The results look good overall, so I think I'm going in the right way

### What's next

In the next two weeks I'll have to:
- Create Particle class with it's logic
- Program that creates particles from an image
- Find a way to turn a video into frames
- Calculate physics from the set of ordered frames and output new frames

Something to have in mind is that it could take me many hours to generate a
 video



## Project Proposal - Nov 5, 2020

[proposal](proposal/)
