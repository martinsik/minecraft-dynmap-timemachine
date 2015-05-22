import dynmap
import time_machine
import os
import unittest
import datetime
import pprint
from peewee import *


class TestTimeMachine(unittest.TestCase):

    @classmethod
    def setup_class(cls):
        cls.dm_majncraft = dynmap.DynMap('http://map.majncraft.cz/')

    def test_capture_single(self):
        pass

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