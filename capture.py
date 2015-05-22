#import PIL
#import urllib
import urllib2
import tempfile
import argparse
import time
import StringIO
import math
import os
import glob
import json
import numpy
import sys
import urlparse
import projection
from PIL import Image

sys.path.append('/usr/local/lib/python2.7/site-packages/')
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('base_url')
parser.add_argument('world')
parser.add_argument('center')
parser.add_argument('width_height_in_tiles')
parser.add_argument('out_dir')
parser.add_argument('-z', '--zoom', default='0')
parser.add_argument('-mt', '--map_type', default='flat')
parser.add_argument('-cs', '--capture_status', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')

args = parser.parse_args()
#print args

if args.quiet:
    sys.stdout = StringIO.StringIO()


opener = urllib2.build_opener()
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'),
]

str_datetime = time.strftime('%Y-%m-%d %H-%M-%S')

tmp_dir = os.path.join(os.path.dirname(__file__), 'tmp')
if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)

out_dir = os.path.realpath(args.out_dir)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

base_url = args.base_url.rstrip('/')
zoom = int(args.zoom)

center_x, center_y, center_z = [int(i) for i in args.center.strip('[]').split(',')]
num_tiles_w, num_tiles_h = [int(i) for i in args.width_height_in_tiles.split(',')]


if args.map_type == 'flat':
    center_x = round(center_x)
    # y axis is reversed
    #center_z = -round(center_z)

    #center_x /= 32 << zoom
    #center_z /= 32 << zoom

    worldtomap = [4.0, 0.0, 0.0, 0.0, 0.0, -4.0, 0.0, 1.0, 0.0]
    minecraft_location = projection.MinecraftLocation(center_x, center_y, center_z, worldtomap)
    tile_location = minecraft_location.to_tile_location(zoom)

elif args.map_type == 't':
    worldtomap = [11.31370849898, 0.0, -11.313708498984, -5.656854249492, 13.85640646055, -5.656854249492, 5.551115123125, 0.99999999999, 5.55111512312578]
    minecraft_location = projection.MinecraftLocation(center_x, center_y, center_z, worldtomap)
    tile_location = minecraft_location.to_tile_location(zoom)

    #center_x /= (9.3*(2**zoom))
    #center_z /= (8.4*(2**zoom))
    #
    #hypotenuse = (center_x ** 2 + center_z ** 2) ** 0.5
    #angle = math.tan(center_z / center_x)
    #if center_x > 0 and center_z < 0:  # top right quadrant
    #    angle = math.radians(30.0) + angle
    #    axis_x, axis_z = (1, -1)
    #
    #print 'debug angle: ' + str(round(math.degrees(angle), 2)) + ' deg'
    #
    #center_x = axis_x * math.cos(angle) * hypotenuse
    #center_z = axis_z * math.sin(angle) * hypotenuse
    #center_z += center_y / 7.111


#from_x, from_z = center_x - num_tiles_w, center_z + num_tiles_h,
#to_x, to_z = center_x + num_tiles_w, center_z - num_tiles_h,

#from_x, from_y = [int(i) for i in args.coords_from.strip('[]').split(',')]
#to_x, to_y = [int(i) + (1 if int(i) >= 0 else -1) for i in args.coords_to.strip('[]').split(',')]
#
#from_x, to_x = sorted([from_x, to_x])
#from_z, to_z = sorted([from_z, to_z])

from_tile, to_tile = tile_location.make_range(zoom, num_tiles_w, num_tiles_h)

print 'range from [%d, %d] to [%d, %d]' % (from_tile.x, from_tile.y, to_tile.x, to_tile.y)

zoomed_scale = projection.zoomed_scale(zoom)
img_map = Image.new('RGB', (abs(to_tile.x - from_tile.x) * 128 / zoomed_scale, abs(to_tile.y - from_tile.y) * 128 / zoomed_scale))

total = 0
# download map
for x in range(from_tile.x, to_tile.x, zoomed_scale):
    for y in range(from_tile.y, to_tile.y, zoomed_scale):
        tile_x = math.floor(x / 32.0)
        tile_y = math.floor(y / 32.0)
        img_url = '%s/tiles/%s/%s/%d_%d/%s%d_%d.png' % (base_url, args.world, args.map_type, tile_x, tile_y, '' if zoom == 0 else ('z' * zoom) + '_', x, y)
        print img_url,
        try:
            response = opener.open(img_url)
            img_data = response.read()
            total += len(img_data)

            print '%d KB' % (len(img_data) / 1000)

            im = Image.open(StringIO.StringIO(img_data))

            # calculate position where we want to place this tile

            box = (abs(x - from_tile.x) * 128 / zoomed_scale, (abs(to_tile.y - y) - zoomed_scale) * 128 / zoomed_scale)

            #print box
            img_map.paste(im, box)
            time.sleep(0.01)
        except urllib2.HTTPError as e:
            print
            if e.code == 404:
                print 'tile doesn\'t exist: %d, %d' % (x, y)
            elif e.code == 500:
                print 'server error'

# check, if there ale already some images in the output directory
files = list(glob.iglob(os.path.join(out_dir, '*.png')))
out_filepath = os.path.join(out_dir, str_datetime + '.png')

print 'total downloaded size: %d KB' % (total / 1000)

if len(files) > 0:  # we have to compare images
    tmp = tempfile.mkstemp(dir=tmp_dir)[1]
    tmp_filepath = tmp + '.png'
    os.rename(tmp, tmp_filepath)
    print 'tmpfile name: ' + tmp_filepath

    img_map.save(tmp_filepath)
    print 'saved .png size: %d KB' % (os.path.getsize(tmp_filepath) / 1000)

    newest = max(files, key=os.path.getctime)
    im_current = cv2.imread(tmp_filepath, 0)
    im_newest = cv2.imread(newest, 0)

    res = cv2.matchTemplate(im_current, im_newest, cv2.TM_CCOEFF_NORMED)
    loc = numpy.where(res < 0.99999)

    print 'opencv match: ' + str(res)

    if len(zip(*loc[::-1])) > 0:  # two compared maps are different
        os.rename(tmp_filepath, out_filepath)
        print 'image saved to: ' + out_filepath
    else:
        os.remove(tmp_filepath)
        print 'no significant difference, image discarded'
else:  # nothing to compare, just save it
    print 'nothing to compare, saving to: ' + out_filepath
    img_map.save(out_filepath)


if args.capture_status:
    parts = list(urlparse.urlparse(base_url))
    parts[2] = '/up/world/MajnujReborn/'

    response = opener.open(urlparse.urlunparse(parts))
    json_str = response.read()
    status = json.loads(json_str)

    if len(status['players']) > 0:
        status_filepath = os.path.join(out_dir, str_datetime + '.json')
        with open(status_filepath, 'w') as f:
            f.write(json_str)
        print 'status saved to: ' + status_filepath
    else:
        print 'no players online, discarded'

