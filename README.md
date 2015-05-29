# Minecraft Dynmap Time Machine

CLI script in Python 3.4 that downloads tiles from a Minecraft's Dynmap plugin HTTP server and composes one image in extremely large resolution suitable for print.

Work in progress.

## Example usage:

Let's say we want to download a 6144x4096 map from [map.majncraft.cz](http://map.majncraft.cz/) at Minecraft position -2000,65,1000.

Full list of parameter's is as follows:

    $ python3.4 main.py -h
    usage: main.py [-h] [--list-worlds] [--list-maps] [-q] [-v] [-vv]
                   base_url [world] [map] [center] [boundary_size] [zoom] [dest]
    
    positional arguments:
      base_url              Dynamp server URL
      world                 world name, use --list-worlds to list available worlds
      map                   map name, use --list-maps to list available maps
      center                minecraft cooridnates, use format: [x,y,z]
      boundary_size         size in tiles, use format: [h,v]
      zoom                  zoom level, 0 = maximum zoom
      dest                  output file name
    
    optional arguments:
      -h, --help            show this help message and exit
      --list-worlds         list available worlds from this Dynmap server and exit
      --list-maps           list available maps for this world and exit

1. First see what worlds are available and what's the name of the world that we want.

   ```
   $ python3.4 main.py --list-worlds http://map.majncraft.cz/
   world - Svět Majncraft | Overworld
   world_space - Vesmír | Space
   world_nether - Nether Reloaded
   ```

   We want the first world on the list called simply `world`.

2. Then list all maps avaialble for this world:

   ```
   $ python3.4 main.py --list-worlds http://map.majncraft.cz/ world
   surface - Prostorová - Den
   surface_night - Prostorová - Noc
   populated - Osídlení světa - prostorové
   flat - Plochá - Den
   populated_flat - Osídlení světa - ploché
   ```
    
   This lists flat, isometric, cave and all other types of maps together. Map names depend on Dynamp's configuration. We want the first one called `surface` which is an isometric map.
   
3. Make a test image with Minecraft's coordinates

   Check your coordinates on Dynmap or simply walk in Minecraft at the position that you want to capture and press F3 to see what are your Minecraft's coordinates:
   
   ```
   python3.4 main.py http://map.majncraft.cz/ world surface [-2000,65,1000] [2,2] 0 majncraft_cz.full.png
   ```
   
   Parameters:
   
   - `http://map.majncraft.cz/` - Dynmap's HTTP server URL
   - `world` - World name
   - `surface` - Map name
   - `[-2000,65,1000]` - Minecraft coordiantes that will be automatically converted to tile names
   - `[2,2]` - Number of tiles I want to download in each direction from specified coordinates. That's two to the left and right, two to the top and bottom. This will actually download 4x4 grid where each tile is 128x128 pixels. In total this image will be 512x512 pixels.
   - `0` - Zoom level. 0 means maximum zoom in. Number of zoom levels depend's on Dynamp's configuration.
   - `majncraft_cz.full.png` - Output file name.
   
   This should generate a 512x512 image (this one is scaled down to 128x128, see [full size image](https://raw.githubusercontent.com/martinsik/minecraft-dynmap-timemachine/master/doc/majncraft_cz.512.png)):
   
   ![Preview from 4x4 grid](https://raw.githubusercontent.com/martinsik/minecraft-dynmap-timemachine/master/doc/majncraft_cz.128.png)
   
4. Make a full size image in 6144x4096 resolution.
   