# import urllib
import json
import time
import math

import re
import simple_downloader


class MapException(Exception):
    def __init__(self, map_obj, *args, **kwargs):
        super(MapException, self).__init__(*args, **kwargs)
        self.map = map_obj


class DynMap(object):

    def __init__(self, url):
        # super(DynMap, self).__init__(*args, **kwargs)
        self.url = url.rstrip('/')

        #self._server_addres = server_addres
        #self._cache_dir = cache_dir
        self._config = None
        self._config_urls = None
        self._worlds = {}

        #self.urls  # force init dynmap urls from server or from property
        self._init()

    def _init(self):
        for c in self.config['worlds']:
            # print(c)
            w = World(c)
            self._worlds[w.name] = w

    def _download_config(self):
        """configuration of all worlds and their maps"""
        rel_path = self.urls['configuration'].replace('{timestamp}', str(int(time.time())))
        return simple_downloader.download(self.url + '/' + rel_path)

    def _download_config_urls(self):
        """DynMap configuration"""
        return simple_downloader.download(self.url + '/' + 'standalone/config.js')

    @staticmethod
    def parse_config_urls_string(jsonlike_str):
        m = re.search('url \: (.+)};', jsonlike_str, re.DOTALL)
        #return json.loads(m.group(1))

        pattern = r"([a-zA-Z_][a-zA-Z_0-9]*)\s*\:"
        repl = lambda match: '"{}":'.format(match.group(1))
        json_str = re.sub(pattern, repl, m.group(1))
        #print json_str
        return json.loads(json_str.replace('\'', '"'))

    @property
    def urls(self):
        if not self._config_urls:
            # if self._config_urls_json:
            #     self._config_urls = json.loads(self._config_urls_json)
            # else:
            self._config_urls = self.parse_config_urls_string(self._download_config_urls())
                # self._config_urls_json = json.dumps(self._config_urls)
                #self.save()

        return self._config_urls

    @property
    def config(self):
        if not self._config:
            # if self._config_json:
            #     self._config = json.loads(self._config_json)
            # else:
            self._config = json.loads(self._download_config())
                # self._config_json = json.dumps(self._config)
        return self._config

    @property
    def worlds(self):
        return self._worlds


class World(object):
    def __init__(self, world_config):
        self._config = world_config
        self._maps = {}
        self._init()

    def _init(self):
        for c in self._config['maps']:
            m = Map(c, self.name)
            self._maps[m.name] = m

    @property
    def name(self):
        return self._config['name']

    @property
    def title(self):
        return self._config['title']

    @property
    def maps(self):
        return self._maps


class Map(object):
    # PERSPECTIVES = ['iso_SE_30_hires', 'iso_SE_30_lowres', 'iso_SE_60_hires', 'iso_SE_60_lowres', 'iso_S_90_hires', 'iso_S_90_lowres']
    # SHADERS = ['stdtexture', 'cave']

    def __init__(self, map_config, world):
        self._config = map_config
        self._world = world
        # if not Map.is_known_perspective(self.perspective):
        #     raise MapException(self, 'Unknown perspective "%s"' % self.perspective)
        # if not Map.is_known_shader(self.shader):
        #     raise MapException(self, 'Unknown shader "%s"' % self.shader)

    # @staticmethod
    # def is_known_perspective(type_name):
    #     return type_name in Map.PERSPECTIVES
    #
    # @staticmethod
    # def is_known_shader(shader_name):
    #     return shader_name in Map.SHADERS

    def image_url(self, t_loc):
        zoom = t_loc.zoom
        chunk_x = math.floor(t_loc.x / 32.0)
        chunk_y = math.floor(t_loc.y / 32.0)
        dashes = ('' if zoom == 0 else ('z' * zoom) + '_')

        image_url = '/tiles/%s/%s/%d_%d/%s%d_%d.png' % (self._world, self.prefix, chunk_x, chunk_y, dashes, t_loc.x, t_loc.y)
        return image_url

    @property
    def perspective(self):
        return self._config['perspective']

    @property
    def shader(self):
        return self._config['shader']

    @property
    def name(self):
        return self._config['name']

    @property
    def title(self):
        return self._config['title']

    @property
    def worldtomap(self):
        return self._config['worldtomap']

    @property
    def prefix(self):
        return self._config['prefix']