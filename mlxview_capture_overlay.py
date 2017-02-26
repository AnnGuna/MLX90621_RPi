# read last line of temp data text file

import numpy as np
import matplotlib.pyplot as plt
import picamera
from PIL import Image
from time import sleep
import time
import gtk.gdk

var = 1
while var <5:

    with picamera.PiCamera() as camera:
        camera.resolution = (500, 400)
        camera.framerate = 24
        camera.capture('/home/pi/mlxd/Photos/background.jpg')

        
    # read data from text file
    file = open('/home/pi/mlxd/testdata.txt','r')
    lineList = file.readlines()
    file.close()

    #map data to heatmap
    data = map(float, lineList[-2].split(','))
    datashape = np.reshape(data,(4,16))

    # create figure
    sizes = np.shape(datashape)
    height = float(sizes[0])
    width = float(sizes[1])
     
    fig = plt.figure()
    fig.set_size_inches(width/height, 1, forward=False)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
 
    ax.imshow(datashape, cmap='hot')
    # ax.imshow(datashape, cmap='hot', interpolation='nearest')
    plt.savefig('/home/pi/mlxd/Photos/tempdata.jpg')
    plt.close()

    # create overlay image
    img = Image.open('/home/pi/mlxd/Photos/tempdata.jpg')
    img_w, img_h = img.size
    background = Image.open('/home/pi/mlxd/Photos/background.jpg')
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
    background.paste(img, offset)
    background.save('/home/pi/mlxd/Photos/image_comb' + str(var) + '.jpg')

    
    var = var +1
