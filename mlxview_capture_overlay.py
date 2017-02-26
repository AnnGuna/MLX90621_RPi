# read last line of temp data text file

#  TO DO
#  ignore nan
#  colorbar and/or
#  overlay in a video

import numpy as np
import matplotlib.pyplot as plt
from matplotlib_colorbar.colorbar import ColorBar
import picamera
from PIL import Image
import ImageEnhance
from time import sleep
import time
import gtk.gdk

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)



var = 1
while var <2:

    with picamera.PiCamera() as camera:
        camera.resolution = (500, 400)
        camera.framerate = 24
        camera.capture('/home/pi/mlxd/Photos/background.jpg')

        
    # read data from text file
    # file = open('/home/pi/mlxd/mlx90620.txt','r')
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
 
    mapped_data = ax.imshow(datashape, cmap='hot')
    # colorbar = ColorBar(mapped_data, location='lower left',bbox_to_anchor=(0.5, 1.05))
    # plt.gca().add_artist(colorbar)
    # plt.show()
    # ax.imshow(datashape, cmap='hot', interpolation='nearest')
    plt.savefig('/home/pi/mlxd/Photos/tempdata.jpg')
    plt.close()

    # create overlay image
    img = Image.open('/home/pi/mlxd/Photos/tempdata.jpg')
    img_w, img_h = img.size
    background = Image.open('/home/pi/mlxd/Photos/background.jpg')
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
    im = watermark(background, img, offset, 0.5)
    im.save('/home/pi/mlxd/Photos/image_comb' + str(var) + '.jpg')

    
    var = var +1
