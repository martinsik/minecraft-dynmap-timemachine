import projection
import os
import unittest


class TestProjection(unittest.TestCase):

    def test_tile_location(self):
        # test range with zoomlevel = 0
        loc = projection.TileLocation(20, 10)
        p_from, p_to = loc.make_range(4, 3)
        self.assertIsInstance(p_from, projection.Location)
        self.assertIsInstance(p_to, projection.Location)
        self.assertEqual(p_from.x, 16)
        self.assertEqual(p_from.y, 7)
        self.assertEqual(p_to.x, 24)
        self.assertEqual(p_to.y, 13)

        loc = projection.TileLocation(20, -10)
        p_from, p_to = loc.make_range(4, 3)
        self.assertEqual(p_from.x, 16)
        self.assertEqual(p_from.y, -13)
        self.assertEqual(p_to.x, 24)
        self.assertEqual(p_to.y, -7)

        loc = projection.TileLocation(-20, 10)
        p_from, p_to = loc.make_range(4, 3)
        self.assertEqual(p_from.x, -24)
        self.assertEqual(p_from.y, 7)
        self.assertEqual(p_to.x, -16)
        self.assertEqual(p_to.y, 13)

        loc = projection.TileLocation(-20, -10)
        p_from, p_to = loc.make_range(4, 3)
        self.assertEqual(p_from.x, -24)
        self.assertEqual(p_from.y, -13)
        self.assertEqual(p_to.x, -16)
        self.assertEqual(p_to.y, -7)

        # test range with zoomlevel = 1
        loc = projection.TileLocation(40, 10, 1)
        p_from, p_to = loc.make_range(4, 3)
        self.assertEqual(p_from.x, 32)
        self.assertEqual(p_from.y, 4)
        self.assertEqual(p_to.x, 48)
        self.assertEqual(p_to.y, 16)

        # test range with zoomlevel = 2
        loc = projection.TileLocation(40, 10, 2)
        p_from, p_to = loc.make_range(4, 3)
        self.assertEqual(p_from.x, 24)
        self.assertEqual(p_from.y, -4)
        self.assertEqual(p_to.x, 56)
        self.assertEqual(p_to.y, 20)


    def test_minecraft_location(self):
        # test iso 30 perspective
        # test wtm on majncraft.cz
        worldtomap = [5.65685424949238, 0, -5.656854249492381, -2.8284271247461907, 6.928203230275509, -2.8284271247461903, 0, 0.9999999999999997, 0]
        m_loc = projection.MinecraftLocation(7600, 65, 100, worldtomap)

        t_loc = m_loc.to_tile_location(0)
        self.assertIsInstance(t_loc, projection.TileLocation)
        self.assertEqual(t_loc.x, 331)
        self.assertEqual(t_loc.y, -168)

        # test zoomlevel = 1
        t_loc = m_loc.to_tile_location(1)
        self.assertEqual(t_loc.x, 332)
        self.assertEqual(t_loc.y, -168)

        # test wtm on majnuj.cz
        worldtomap = [11.31370849898, 0.0, -11.313708498984, -5.656854249492, 13.85640646055, -5.656854249492, 5.551115123125, 0.99999999999, 5.55111512312578]
        t_loc = projection.MinecraftLocation(-1013, 65, 702, worldtomap).to_tile_location(0)
        self.assertEqual(t_loc.x, -152)
        self.assertEqual(t_loc.y, 20)

        t_loc = projection.MinecraftLocation(1280, 65, -370, worldtomap).to_tile_location(0)
        self.assertEqual(t_loc.x, 146)
        self.assertEqual(t_loc.y, -34)

        # test flat map on majnuj.cz
        worldtomap = [4.0, 0.0, 0.0, 0.0, 0.0, -4.0, 0.0, 1.0, 0.0]
        t_loc = projection.MinecraftLocation(1280, 65, -370, worldtomap).to_tile_location(0)
        self.assertEqual(t_loc.x, 40)
        self.assertEqual(t_loc.y, 11)
