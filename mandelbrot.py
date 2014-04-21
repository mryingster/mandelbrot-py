#!/usr/bin/env python
import sys, math, cairo

# Exit with error message
def die(message):
    print "ERROR:", message
    quit()

# Generate Table for spectrum of colors
def genSpectrum(c, depth):
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

# Generate gradient based on user input
def genNonlinearGradient(c1, c2, depth):
    colors = []
    r, g, b = c1
    rRange = float((c2[0] - c1[0]))
    gRange = float((c2[1] - c1[1]))
    bRange = float((c2[2] - c1[2]))
    for i in range(depth):
        colors.append([r/255.0, g/255.0, b/255.0])
        multiplier = float(math.sqrt((i+1.0)/depth))
        r = c1[0]+(rRange*multiplier)
        g = c1[1]+(gRange*multiplier)
        b = c1[2]+(bRange*multiplier)
    return colors

def genLinearGradient(c1, c2, depth):
    colors = []
    r, g, b = c1
    rInc = float((c2[0] - c1[0]) / depth)
    gInc = float((c2[1] - c1[1]) / depth)
    bInc = float((c2[2] - c1[2]) / depth)
    for i in range(depth+1):
        colors.append([r/255.0, g/255.0, b/255.0])
        r += rInc
        g += gInc
        b += bInc
    return colors

# Parse Arguments
import argparse
parser = argparse.ArgumentParser(description='Use this script to generate mandelbrot images.')
parser.add_argument('--output', '-o',                      default = "mandelbrot.png"        , help='Specify output PNG filename. (default: %(default)s)')
parser.add_argument('--width',        type=int,            default = 512                     , help='Specify image width in pixels. Maximum is 24889. (default: %(default)s)')
parser.add_argument('--coord',        type=float, nargs=4, default = [-2.25, 1.3, .75, -1.3] , help='Specify rectangular coordinates for view (default: %(default)s)', metavar=('x1', 'y1', 'x2', 'y2'))
parser.add_argument('--color',        type=int, nargs=6,   default = [255, 0, 0, 255, 255, 0], help='Specify gradient starting and ending values (0-255 for r, g, and b). (default: %(default)s)',         metavar=('R', 'G', 'B', 'R', 'G', 'B'))
parser.add_argument('--depth',        type=int,            default = 125                     , help='Specify how many levels to calculate each point. (default: %(default)s)')

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
for i in range(6):
    if options.color[i] < 0 or options.color[i] > 255:
        die("Invalid color value,")
colorTable = genNonlinearGradient(options.color[0:3], options.color[3:6], options.depth)

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
            red, green, blue = 0,0,0
        else:
            red, green, blue = colorTable[depth]
        ctx.set_source_rgb(red, green, blue)
        ctx.rectangle(x,y,1,1)
        ctx.fill()
    print "\r%i%% Complete" % int(((y+1)*100)/pixelHeight),
    sys.stdout.flush()

# Write Output File
surface.write_to_png(options.output)
