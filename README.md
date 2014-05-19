Mandelbrot Py
=============

Description
-----------
Mandelbrot is a mandelbrot generator written in Python (2). It will output an image to a PNG formatted file.

Dependencies
------------
 * Py2Cairo --- A graphics library

Options
-------
  `-h`, `--help` --- Show this help message and exit
  `--output filename.png`, `-o filename.png` --- Specify output PNG filename. (default: mandelbrot.png)
  `--width n` --- Specify image width in pixels. Maximum is 24889. (default: 512)
  `--coord x1 y1 x2 y2` --- Specify rectangular coordinates for view (default: [-2, 2, 2, -2])
  `--color R G B R G B` --- Specify gradient starting and ending values (0-255 for r, g, and b). (default: [255, 0, 0, 255, 255, 0])
  `--colorm R G B` --- Specify color for points that fall in the mandelbrot series. (default: [0, 0, 0])
  `--depth n` ---  Specify how many levels to calculate each point. (default: 125)
  `--random` --- Use random colors when generating image
  `--spectrum` --- Use color spectrum when generating image
