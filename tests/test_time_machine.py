import unittest
import os
from PIL import Image
from minecraft_dynmap_timemachine import dynmap
from minecraft_dynmap_timemachine import time_machine
from minecraft_dynmap_timemachine import projection

_path = os.path.dirname(__file__)

class TestTimeMachine(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.dm_majncraft = dynmap.DynMap('http://map.majncraft.cz/')

    def test_capture_single(self):
        maps = self.dm_majncraft.worlds['world'].maps
        tm = time_machine.TimeMachine(self.dm_majncraft)

        m_loc = projection.MinecraftLocation(-5000, 65, 8000, maps['surface'].worldtomap)
        self._test_downloaded_image(maps['surface'], tm, m_loc, 1)

        # check border missing tiles
        m_loc = projection.MinecraftLocation(-5100, 65, 8100, maps['surface'].worldtomap)
        self._test_downloaded_image(maps['surface'], tm, m_loc, 0)


    def _test_downloaded_image(self, map, tm, m_loc, zoom):
        img = tm.capture_single(map, m_loc.to_tile_location(zoom), (2,2))

        self.assertTupleEqual(img.size, (512, 512))
        self.assertGreater(len(img.tobytes()), 100 * 1000)

    def test_compare_images(self):
        tm = time_machine.TimeMachine(self.dm_majncraft)
        result = tm.compare_images(Image.open(os.path.join(_path, 'flat.test.1.png'), 'r'), Image.open(os.path.join(_path, 'flat.test.2.png'), 'r'))
        self.assertGreater(0.0004, result)

        result = tm.compare_images(Image.open(os.path.join(_path, 'flat.test.2.png'), 'r'), Image.open(os.path.join(_path, 'flat.test.3.png'), 'r'))
        self.assertGreater(0.0004, result)

        result = tm.compare_images(Image.open(os.path.join(_path, 'flat.test.3.png'), 'r'), Image.open(os.path.join(_path, 'flat.test.4.png'), 'r'))
        self.assertGreater(0.0008, result)

        result = tm.compare_images(Image.open(os.path.join(_path, 'surface.test.1.png'), 'r'), Image.open(os.path.join(_path, 'surface.test.2.png'), 'r'))
        self.assertGreater(0.0025, result)

        result = tm.compare_images(Image.open(os.path.join(_path, 'surface.test.1.png'), 'r'), Image.open(os.path.join(_path, 'surface.test.3.png'), 'r'))
        self.assertGreater(0.0045, result)

        result = tm.compare_images(Image.open(os.path.join(_path, 'surface.test.3.png'), 'r'), Image.open(os.path.join(_path, 'surface.test.4.png'), 'r'))
        self.assertGreater(0.019, result)

    # @classmethod
    # def setup_class(cls):
    #     cls._db_dynmap_name = 'test_dynmap.db'
    #     try:
    #         os.remove(cls._db_dynmap_name)
    #     except:
    #         pass
    #
    #     cls._db = SqliteDatabase(cls._db_dynmap_name)
    #     time_machine.database_proxy.initialize(cls._db)
    #     dynmap.database_proxy.initialize(cls._db)
    #
    #     dynmap.DynMap.create_table()
    #     time_machine.Timelapse.create_table()
    #     time_machine.Task.create_table()
    #
    #     cls._dm = dynmap.DynMap(url='http://map.majncraft.cz/')
    #     cls._dm.save()
    #
    #     cls._tl = time_machine.Timelapse.create(dynmap=cls._dm, center_x=0, center_y=0, zoom=1, width=3, height=2, world_name='Majnuj', map_name='surface', frequency=1)
    #     cls._tl.save()
    #
    #     cls._t1 = time_machine.Task.create(timelapse=cls._tl, scheduled=datetime.datetime.now() - datetime.timedelta(minutes=1))
    #     cls._t1.save()
    #     cls._t2 = time_machine.Task.create(timelapse=cls._tl, scheduled=datetime.datetime.now() + datetime.timedelta(minutes=1))
    #     cls._t2.save()
    #
    #     cls._tm = time_machine.TimeMachine()
    #
    #     #cls._tm.save()
    #
    # @classmethod
    # def teardown_class(cls):
    #     cls._db.close()
    #     os.remove(cls._db_dynmap_name)
    #
    # def test_get_scheduled_tasks(self):
    #     tasks = [t for t in self._tm.get_scheduled_tasks()]
    #
    #     self.assertEqual(len(tasks), 1)
    #     self.assertEqual(self._t1.id, tasks[0].id)
    #
    # def test_get_tile_url(self):
    #     pprint.pprint(self._dm.config)
    #
    # def test_timelapse_capture(self):
    #     pass