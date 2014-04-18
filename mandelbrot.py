#!/usr/bin/python
import sys, math, cairo

def die(message):
    print "ERROR:", message
    quit()

if len(sys.argv) == 7:
    xL = float(sys.argv[1])
    yU = float(sys.argv[2])
    xU = float(sys.argv[3])
    yL = float(sys.argv[4])
    #print xL, yU, xU, yL
    if xL >= xU:
        die("Invalid x coordinates")
    if yL >= yU:
        die("Invalid Y coordinates")
    pixelWidth = int(sys.argv[5])
    if pixelWidth <1:
        die("Invalid image width (px)")
    outputName=sys.argv[6]
elif len(sys.argv) == 2:
    #Top Left Coordinate
    xL, yU = -2.25, 1.3 # -.29, .98 #
    #Bottom Right Coordinate
    xU, yL = .75, -1.3 # 0.06, .6 #
    pixelWidth  = 512
    outputName=sys.argv[1]
else:
    die ("Please provide output filename.")

# Sizes - Calculate sizes
xRange = xU - xL
yRange = yU - yL
pixelHeight = int(pixelWidth/xRange*yRange)
step   = xRange / ( pixelWidth - 1.0 )
depth  = 125
startColor=0xff0000
colorIncrement = 1024/depth

#Setup Cairo
surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, pixelWidth, pixelHeight)
ctx = cairo.Context (surface)

def hex_to_rgb(value):
    value = "%06x"%value
    lv = len(value)
    return [int(value[i:i+lv/3], 16) for i in range(0, lv, lv/3)]

def rgb_to_hex(value):
    return value[0]*0x10000 + value[1]*0x100 + value[2]

def formatColor(inputColor):
    if inputColor == None: return "255 255 255"
    outputColor = "%06x"%inputColor
    return str(int(outputColor[0:2],16))+" "+str(int(outputColor[2:4],16))+" "+str(int(outputColor[4:6],16))

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
    return colors#float(c[0]/255.0), float(c[1]/255.0), float(c[2]/255.0)

colorTable=genColor(startColor)

def mandel(xP, yP, x, y):
    xOut = (xP ** 2) + x - (yP ** 2)
    yOut = 2 * xP * yP + y
    return xOut, yOut

#Process Array
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

#Output File
surface.write_to_png(outputName)
