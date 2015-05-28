# Minecraft Dynmap Time Machine

CLI script in Python 3.4 that downloads tiles from a Minecraft's Dynmap plugin HTTP server and composes one image in extremely large resolution suitable for print.

Work in progress.

## Example usage:

Let's say we want to download a 4096x4096 map from [map.majncraft.cz](http://map.majncraft.cz/) at Minecraft position 1000,65,300.

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
$ python3.4 main.py --list-worlds http://map.majncraft.cz/ world surface [0,0,0] [6,4] 3 test.png
surface - Prostorová - Den
surface_night - Prostorová - Noc
populated - Osídlení světa - prostorové
flat - Plochá - Den
populated_flat - Osídlení světa - ploché
```
    
   This lists flat and ortogonal maps together. We want for example the first one called `surface`.