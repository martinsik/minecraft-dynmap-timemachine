import logging
import argparse
import dynmap
import time_machine
import projection
import sys
import os

# logger = logging.getLogger('')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('base_url', help='Dynamp server URL')
    parser.add_argument('world', nargs='?', help='world name, use --list-worlds to list available worlds')
    parser.add_argument('map', nargs='?', help='map name, use --list-maps to list available maps')
    parser.add_argument('center', nargs='?', help='minecraft cooridnates, use format: [x,y,z]')
    parser.add_argument('boundary_size', nargs='?', help='size in tiles, use format: [h,v]')
    parser.add_argument('zoom', nargs='?', default='0', help='zoom level, 0 = maximum zoom')
    parser.add_argument('dest', nargs='?', help='output file name')
    # parser.add_argument('out_dir')
    # parser.add_argument('-t', '--type', default='flat')
    parser.add_argument('--list-worlds', action='store_true', help='list available worlds from this Dynmap server and exit')
    parser.add_argument('--list-maps', action='store_true', help='list available maps for this world and exit')
    # parser.add_argument('-cs', '--capture_status', action='store_true')
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-vv', '--verbose-debug', action='store_true')

    args = parser.parse_args()


    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if args.verbose_debug:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('args: %s', str(args))


    dm = dynmap.DynMap(args.base_url)

    if args.list_worlds:
        worlds = dm.worlds
        logging.info('available worlds: %s', str(worlds))
        for name in worlds.keys():
            print('%s - %s' % (name, worlds[name].title))
        sys.exit(0)

    if args.world:
        if not args.world:
            logging.error('no world set, use: main.py http://dynmap-address world_name')
            sys.exit(1)
        if args.world not in dm.worlds.keys():
            logging.error('This world doesn\'t exist.\nAvailable worlds: %s', dm.worlds.keys())
            sys.exit(1)

        if args.list_maps:
            logging.info('available maps for world "%s": %s', args.world, dm.worlds[args.world].maps)
            maps = dm.worlds[args.world].maps
            for name in maps.keys():
                print('%s - %s' % (name, maps[name].title))
            sys.exit(0)

    if args.world and args.map and args.center and args.boundary_size and args.dest and args.zoom:
        maps = dm.worlds[args.world].maps

        if args.map not in maps.keys():
            logging.error('map not found, use: main.py http://dynmap-address world_name map_name [x,y,z] [width,height]')
            for name in maps.keys():
                print('%s - %s' % (name, maps[name].title))
            sys.exit(1)

        center = [int(i) for i in args.center.strip('[]').split(',')]
        size = [int(i) for i in args.boundary_size.strip('[]').split(',')]
        # print(size)
        # sys.exit(-1)

        dm_map = maps[args.map]
        m_loc = projection.MinecraftLocation(center[0], center[1], center[2], dm_map.worldtomap)

        tm = time_machine.TimeMachine(dm)
        dest = args.dest
        zoom = int(args.zoom)
        img = tm.capture_single(dm_map, m_loc.to_tile_location(zoom), size)
        img.save(dest)

        logging.info('saving image to "%s" (%d KB)', dest, os.path.getsize(dest) / 1000)

        sys.exit(0)
