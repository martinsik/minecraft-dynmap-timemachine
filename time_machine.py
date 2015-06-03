import dynmap
import logging
import time
import projection
import simple_downloader
import io
import os
from PIL import Image


class TimeMachine(object):

    def __init__(self, dm_map):
        self._dm_map = dm_map
        # self.dynmap = dynmap.DynMap(url)

    def capture_single(self, map, t_loc, size, pause=0.25):
        from_tile, to_tile = t_loc.make_range(size[0], size[1])
        zoomed_scale = projection.zoomed_scale(t_loc.zoom)

        width, height = (abs(to_tile.x - from_tile.x) * 128 / zoomed_scale, abs(to_tile.y - from_tile.y) * 128 / zoomed_scale)
        logging.info('final size in px: [%d, %d]', width, height)
        dest_img = Image.new('RGB', (int(width), int(height)))

        logging.info('downloading tiles...')
        # logging.info('tile image path: %s', image_url)
        total_tiles = len(range(from_tile.x, to_tile.x, zoomed_scale)) * len(range(from_tile.y, to_tile.y, zoomed_scale))
        processed = 0

        for x in range(from_tile.x, to_tile.x, zoomed_scale):
            for y in range(from_tile.y, to_tile.y, zoomed_scale):
                img_rel_path = map.image_url(projection.TileLocation(x, y, t_loc.zoom))
                img_url = self._dm_map.url + img_rel_path

                processed += 1
                logging.info('tile %d/%d [%d, %d]', processed, total_tiles, x, y)

                try:
                    img_data = simple_downloader.download(img_url, True)
                except Exception as e:
                    logging.info('Unable to download "%s": %s', img_url, str(e))
                    continue

                stream = io.BytesIO(img_data)
                im = Image.open(stream)

                box = (int(abs(x - from_tile.x) * 128 / zoomed_scale), int((abs(to_tile.y - y) - zoomed_scale) * 128 / zoomed_scale))
                logging.debug('place to [%d, %d]', box[0], box[1])
                dest_img.paste(im, box)

                # avoid throttle limit, don't overload the server
                time.sleep(float(pause))

        return dest_img


    def compare_with_images(self, filepath):
        import cv2
        import numpy

        tmp_filepath = tempfile.mkstemp(dir=tmp_dir)[1] + '.png'

        img_map.save(tmp_filepath)

        newest = max(files, key=os.path.getctime)
        im_current = cv2.imread(tmp_filepath, 0)
        im_newest = cv2.imread(newest, 0)

        res = cv2.matchTemplate(im_current, im_newest, cv2.TM_CCOEFF_NORMED)
        loc = numpy.where(res < 0.99999)

        print('opencv match: ' + str(res))

        if len(zip(*loc[::-1])) > 0:  # two compared maps are different
            os.rename(tmp_filepath, out_filepath)
            # print 'image saved to: ' + out_filepath
        else:
            os.remove(tmp_filepath)
            # print 'no significant difference, image discarded'
