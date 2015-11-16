# -*- coding: utf-8 -*-

import unittest
from minecraft_dynmap_timemachine import dynmap
from minecraft_dynmap_timemachine import projection


class TestDynMapClassMethods(unittest.TestCase):
    def test_dynmap_parse_config_urls(self):
        config_urls = dynmap.DynMap.parse_config_urls_string("var config = { url : { key: \"value\" } };")
        self.assertIsInstance(config_urls, dict)
        self.assertTrue('key', config_urls)
        self.assertTrue(config_urls['key'], 'value')


class TestDynMap(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        # cls._db_dynmap_name = 'test_dynmap.db'
        # try:
        #     os.remove(cls._db_dynmap_name)
        # except:
        #     pass
        # cls._db = SqliteDatabase(cls._db_dynmap_name)

        # dynmap.database_proxy.initialize(cls._db)
        # dynmap.DynMap.create_table()

        cls.dm_majncraft = dynmap.DynMap('http://map.majncraft.cz/')
        # cls.dm_majncraft.save()

    # @classmethod
    # def teardown_class(cls):
    #     cls._db.close()
    #     os.remove(cls._db_dynmap_name)

    def test_dynmap_config_majncraft_cz(self):
        config_urls = self.dm_majncraft.urls
        # self.dm_majncraft.save()
        # self.assertGreater(len(self.dm_majncraft.config_urls_json), 0)
        self.assertIn('configuration', config_urls)
        self.assertIn('update', config_urls)
        self.assertIn('tiles', config_urls)
        self.assertIn('markers', config_urls)

        # global dm_majnuj_cz
        config = self.dm_majncraft.config
        # self.dm_majncraft.save()
        # self.assertGreater(len(self.dm_majncraft.config_json), 0)
        self.assertIn('worlds', config)
        self.assertIn('dynmapversion', config)
        self.assertIn('coreversion', config)
        self.assertIn('title', config)

    def test_worlds_majncraft_cz(self):
        worlds = self.dm_majncraft.worlds
        self.assertGreaterEqual(len(worlds), 3)  # assume there's a few of them. Modify if needed.
        self.assertIn('world', worlds)
        self.assertEqual(worlds['world'].name, 'world')
        self.assertEqual(worlds['world'].title, u'Eternia | Overworld')

        print()
        for name in worlds.keys():
            print(name, ' - ', worlds[name].title)

    def test_maps_majncraft_cz(self):
        maps = self.dm_majncraft.worlds['world'].maps
        self.assertGreater(len(maps), 0)
        # self.assertTrue(dynmap.Map.is_known_perspective(maps['surface'].perspective))
        # self.assertTrue(dynmap.Map.is_known_shader(maps['surface'].shader))

        self.assertEqual(maps['surface'].name, 'surface')
        self.assertEqual(maps['surface'].title, u'Prostorová - Den')
        self.assertGreater(len(maps['surface'].worldtomap), 0)

        # test unknown perspective and shader
        # self.assertRaises(dynmap.MapException, dynmap.Map, {'perspective': 'fake_perspective', 'shader': 'stdtexture'})
        # self.assertRaises(dynmap.MapException, dynmap.Map, {'perspective': 'iso_SE_60_hires', 'shader': 'fake_shader'})

        print()
        for name in maps.keys():
            print(name, ' - ', maps[name].title)

    def test_worldtomap(self):
        dm_map = self.dm_majncraft.worlds['world'].maps['surface']

        self.assertIsInstance(dm_map.worldtomap, list)
        self.assertEqual(len(dm_map.worldtomap), 9)

    def test_map_image_url(self):
        dm_map = self.dm_majncraft.worlds['world'].maps['surface']
        m_loc = projection.MinecraftLocation(3020, 65, 700, dm_map.worldtomap)
        t_loc = m_loc.to_tile_location(0)

        print()
        print(dm_map.image_url(t_loc))

        t_loc = m_loc.to_tile_location(1)
        print(dm_map.image_url(t_loc))

        t_loc = m_loc.to_tile_location(2)
        print(dm_map.image_url(t_loc))

        dm_map = self.dm_majncraft.worlds['world'].maps['flat']
        m_loc = projection.MinecraftLocation(3020, 65, 700, dm_map.worldtomap)
        t_loc = m_loc.to_tile_location(0)
        print(dm_map.image_url(t_loc))

        t_loc = m_loc.to_tile_location(1)
        print(dm_map.image_url(t_loc))

        t_loc = m_loc.to_tile_location(2)
        print(dm_map.image_url(t_loc))
