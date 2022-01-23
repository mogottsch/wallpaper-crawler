## Wallpaper Crawler

This python script downloads a landscape wallpaper from
[pexels](https://www.pexels.com/) and ensures with the help of the open source
neural network framework [darknet](https://github.com/AlexeyAB/darknet) that
there are no people on the image.

### Why?

When I switched from Windows 10 to Linux I really missed the beatiful landscape
images on the login screen. I wanted to have that on Linux again. I couldn't
find a solution, so I decided to create a script that downloads the images.
With the help of [lightdm](https://wiki.archlinux.org/title/LightDM) I now a
beatiful and varying login screen again.  
The only problem was that pexels category "landscapes" sometimes had images of
old people working out. That was not only unpleasent to watch, but sometimes
even embarassing. Therefore I added object detection to throw away images with
people.
