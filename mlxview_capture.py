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
    # read data from text file
    file = open('/home/pi/mlxd/mlx90620.txt','r')
    lineList = file.readlines()
    file.close()

    # create figure
    fig = plt.figure(frameon=False)
    ax = plt.Axes(fig, [0.,0.,1.,1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    #map data to heatmap
    data = map(float, lineList[-2].split(','))
    datashape = np.reshape(data,(4,16))
    image = ax.imshow(datashape, cmap='hot')
    plt.savefig('/home/pi/mlxd/tempdata.jpg')
    file.close()
    overlay = Image.open('/home/pi/mlxd/tempdata.jpg')
    
    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.start_preview()

        img = Image.open('/home/pi/mlxd/tempdata.jpg')
        pad = Image.new('RGB', (
            ((img.size[0] + 31) // 32) * 32,
            ((img.size[1] + 15) // 16) * 16,
            ))
        pad.paste(img, (0, 0))
        o = camera.add_overlay(pad.tostring(), size=img.size)
        o.alpha = 128
        o.layer = 3



        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        print "The size of the window is %d x %d" % sz
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb != None):
            pb.save('/home/pi/mlxd/Photos/image_comb' + str(var) + '.png',"png")
            print "Screenshot saved to screenshot."
        else:
            print "Unable to get the screenshot."

        # camera.capture('/home/pi/mlxd/Photos/image_comb' + str(var) + '.jpg')
        time.sleep(1)
        camera.stop_preview()
    var = var +1
