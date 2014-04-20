#!/usr/bin/env python
import sys, math, cairo

# Exit with error message
def die(message):
    print "ERROR:", message
    quit()

# Generate Table of Incrementing Hues
def genColor(c):
    colors=[]
    for i in range(1536):
        if   c[0] == 255 and c[1] <  255 and c[2] == 0:                 c[1]+=1  #Red to yellow
        elif c[0] <= 255 and c[1] == 255 and c[2] == 0   and c[0] != 0: c[0]-=1  #yellow to green
        elif c[0] == 0   and c[1] == 255 and c[2] <  255:               c[2]+=1  #green to cyan
        elif c[0] == 0   and c[1] <= 255 and c[2] == 255 and c[1] != 0: c[1]-=1  #cyan to blue
        elif c[0] <  255 and c[1] == 0   and c[2] == 255:               c[0]+=1  #blue to purple
        elif c[0] == 255 and c[1] == 0   and c[2] <= 255 and c[2] != 0: c[2]-=1  #purple to red
        colors.append([float(c[0]/255.0), float(c[1]/255.0), float(c[2]/255.0)])
    return colors

# Parse Arguments
import argparse
parser = argparse.ArgumentParser(description='Use this script to generate mandelbrot images.')
parser.add_argument('--output', '-o',                      default = "mandelbrot.png"       , help='Specify output PNG filename. (default: %(default)s)')
parser.add_argument('--width',        type=int,            default = 512                    , help='Specify image width in pixels. Maximum is 24889. (default: %(default)s)')
parser.add_argument('--coord',        type=float, nargs=4, default = [-2.25, 1.3, .75, -1.3], help='Specify rectangular coordinates for view (default: %(default)s)', metavar=('x1', 'y1', 'x2', 'y2'))
parser.add_argument('--color',        type=int, nargs=3,   default = [255, 0, 0]            , help='Specify gradient starting color. (default: %(default)s)')
parser.add_argument('--colors',       type=int,            default = 1024                   , help='Specify number of colors in spectrum gradient. The ' +
                                                                                                   'gradient cycles through the spectrum in 1530 steps (default: %(default)s)')
parser.add_argument('--depth',        type=int,            default = 125                    , help='Specify how many levels to calculate each point. (default: %(default)s)')

options = parser.parse_args()

# Setup Sizes
xL, yU, xU, yL = options.coord
if xL >= xU: die("Invalid x coordinates")
if yL >= yU: die("Invalid Y coordinates")
if options.width <1: die("Invalid image width (px)")
xRange = xU - xL
yRange = yU - yL
pixelHeight = int(options.width/xRange*yRange)
step = xRange / ( options.width - 1.0 )

# Setup Color
for i in range(3):
    if options.color[i] < 0 or options.color[i] > 255:
        die("Invalid color value,")
colorIncrement = options.colors/options.depth
colorTable = genColor(options.color)

# Setup Cairo
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, options.width, pixelHeight)
ctx = cairo.Context (surface)

# Mandelbrot Calculation
def mandel(x, y, depth):
    limit = 10
    xP, yP = 0, 0
    for i in range(depth):
        xT = (xP ** 2) + x - (yP ** 2)
        yT = 2 * xP * yP + y
        if abs(xT) > limit or abs(yT) > limit:
            return i
        xP, yP = xT, yT
    return -1

# Process Mandelbrot Image
for y in range(0, pixelHeight):
    for x in range(0, options.width):
        xValue, yValue = (xL+(x*step)), (yU-(y*step))
        depth=mandel(xValue, yValue, options.depth)
        if depth == -1:
            ctx.set_source_rgb(0,0,0)
        else:
            red, green, blue = colorTable[depth*colorIncrement]
            ctx.set_source_rgb(red, green, blue)
        ctx.rectangle(x,y,1,1)
        ctx.fill()
    print "\r%i%% Complete" % int(((y+1)*100)/pixelHeight),
    sys.stdout.flush()

# Write Output File
surface.write_to_png(options.output)
