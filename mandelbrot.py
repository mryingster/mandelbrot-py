#!/usr/bin/python
import sys, math, cairo

# Exit with error message
def die(message):
    print "ERROR:", message
    quit()

# Convert HEX value to RGB values
def hex_to_rgb(value):
    value = "%06x"%value
    lv = len(value)
    return [int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3)]

# Generate Table of Incrementing Hues
def genColor(startColor):
    colors=[]
    c = hex_to_rgb(startColor)
    for i in range(1536):
        if c[0] == 255 and c[1] < 255 and c[2] == 0:                  c[1]+=1  #Red to yellow
        elif c[0] <= 255 and c[1] == 255 and c[2] == 0 and c[0] != 0: c[0]-=1  #yellow to green
        elif c[0] == 0 and c[1] == 255 and c[2] < 255:                c[2]+=1  #green to cyan
        elif c[0] == 0 and c[1] <= 255 and c[2] == 255 and c[1] != 0: c[1]-=1  #cyan to blue
        elif c[0] < 255 and c[1] == 0 and c[2] == 255:                c[0]+=1  #blue to purple
        elif c[0] == 255 and c[1] == 0 and c[2] <= 255 and c[2] != 0: c[2]-=1  #purple to red
        colors.append([float(c[0]/255.0), float(c[1]/255.0), float(c[2]/255.0)])
    return colors

# Setup Defualt Values
xL, yU = -2.25, 1.3 # -.29, .98 ##Top Left Coordinate
xU, yL = .75, -1.3 # 0.06, .6 ##Bottom Right Coordinate
pixelWidth = 512
startColor = 0xff0000

# Parse Arguments
skip=0
for i in range(1, len(sys.argv)):
    if skip > 0:
        skip-=1
        continue
    if sys.argv[i] == "--coord":
        if len(sys.argv) <= i+4:
            die("Not enough arguments supplied.")
        try:
            xL = float(sys.argv[i+1])
            yU = float(sys.argv[i+2])
            xU = float(sys.argv[i+3])
            yL = float(sys.argv[i+4])
        except:
            die("Invalid coordinates")
        if xL >= xU:
            die("Invalid x coordinates")
        if yL >= yU:
            die("Invalid Y coordinates")
        skip=4
    elif sys.argv[i] == "--width":
        try:
            pixelWidth = int(sys.argv[i+1])
        except:
            die("Invalid width value.")
        if pixelWidth <1:
            die("Invalid image width (px)")
        skip=1
    elif sys.argv[i] == "--color":
        try:
            startColor=int(sys.argv[i+1],16)
        except:
            die("Invalid color.")
        skip=1
    elif sys.argv[i] == "-o":
        outputName=sys.argv[i+1]
        skip=1
    elif sys.argv[i] == "-h":
        print "SHOW HELP"
    else:
        die ("Unknown option, \"%s\". Please try -h for help." % sys.argv[i])

# Setup Sizes
xRange = xU - xL
yRange = yU - yL
pixelHeight = int(pixelWidth/xRange*yRange)
step = xRange / ( pixelWidth - 1.0 )
depth = 125

# Setup Color
colorIncrement = 1024/depth
colorTable = genColor(startColor)

# Setup Cairo
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, pixelWidth, pixelHeight)
ctx = cairo.Context (surface)

# Mandelbrot Calculation
def mandel(xP, yP, x, y):
    xOut = (xP ** 2) + x - (yP ** 2)
    yOut = 2 * xP * yP + y
    return xOut, yOut

# Process Mandelbrot Image
for y in range(0, pixelHeight):
    for x in range(0, pixelWidth):
        xValue, yValue = (xL+(x*step)), (yU-(y*step))
        xP, yP = 0, 0
        isMandelbrot = 0
        for i in range(depth):
            xP, yP = mandel(xP, yP, xValue, yValue)
            if abs(xP) > 10 or abs(yP) > 10:
                red, green, blue = colorTable[i*colorIncrement]
                ctx.set_source_rgb(red, green, blue)
                isMandelbrot=1
                break
        if isMandelbrot == 0:
            ctx.set_source_rgb(0,0,0)
        ctx.rectangle(x,y,1,1)
        ctx.fill()
    print "\r%i%% Complete" % int((y*100)/pixelHeight),
    sys.stdout.flush()

# Write Output File
surface.write_to_png(outputName)
