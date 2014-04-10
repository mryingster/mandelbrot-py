#!/usr/bin/python
import math

# Sizes - Calculate sizes
#Top Left Coordinate
xL, yU = -2.25, 1.35 # -.29, .98 #
#Bottom Right Coordinate
xU, yL = 0.85, -1.35 # 0.06, .6 #
xRange = xU - xL
yRange = yU - yL
pixelWidth  = 25000
pixelHeight = int(pixelWidth/xRange*yRange)
step   = xRange / ( pixelWidth - 1.0 )
depth  = 100
startColor=0x0000ff
colorIncrement = 1024/depth

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

def colorTableGen(color):
    colors=[]
    c = hex_to_rgb(color)
    for i in range(1530):
        if c[0] == 255 and c[1] < 255 and c[2] == 0:                  c[1]+=1  #Red to yellow
        elif c[0] <= 255 and c[1] == 255 and c[2] == 0 and c[0] != 0: c[0]-=1  #yellow to green
        elif c[0] == 0 and c[1] == 255 and c[2] < 255:                c[2]+=1  #green to cyan
        elif c[0] == 0 and c[1] <= 255 and c[2] == 255 and c[1] != 0: c[1]-=1  #cyan to blue
        elif c[0] < 255 and c[1] == 0 and c[2] == 255:                c[0]+=1  #blue to purple
        elif c[0] == 255 and c[1] == 0 and c[2] <= 255 and c[2] != 0: c[2]-=1  #purple to red
        colors.append(str(formatColor(rgb_to_hex(c))))
    return colors

Colors=colorTableGen(startColor)

def mandel(xP, yP, x, y):
    #print xP, yP, x, y
    xOut = (xP ** 2) + x - (yP ** 2)
    yOut = 2 * xP * yP + y
    return xOut, yOut

#Print PPM
print "P3"                        # File Type
print pixelWidth, pixelHeight
print "255"                       # Bit Depth

#Process Array
for y in range(0, pixelHeight):
    for x in range(0, pixelWidth):
        xValue, yValue = (xL+(x*step)), (yU-(y*step))
        xP, yP = 0, 0
        isMandelbrot = 0
        for i in range(depth):
            xP, yP = mandel(xP, yP, xValue, yValue)
            if abs(xP) > 10 or abs(yP) > 10:
                print Colors[(i-1)*colorIncrement],
                isMandelbrot=1
                break
        if isMandelbrot == 0:
            print "0 0 0",
    print
