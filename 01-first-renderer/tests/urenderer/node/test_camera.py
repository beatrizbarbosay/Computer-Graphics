import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

import urenderer


class TestCamera(unittest.TestCase):
    def test_projection_matrix(self) -> None:
        camera = urenderer.node.Camera()

        camera.near_plane = 1.0
        camera.far_plane = 10.0
        camera.screen_width = 1920.0
        camera.screen_height = 1080.0
        camera.vertical_fov = 60.0

        matrix = np.array([[0.974279,  0.,  0.,  0.],
                           [0.,  1.732051,  0.,  0.],
                           [0.,  0., -1.222222, -2.222222],
                           [0.,  0., -1.,  0.]])

        assert_array_almost_equal(camera.projection_matrix, matrix)

        camera.near_plane = 1.123
        camera.far_plane = 321.0
        camera.screen_width = 456.0
        camera.screen_height = 789.0
        camera.vertical_fov = 90.0

        matrix = np.array([[1.730263,  0.,  0.,  0.],
                           [0.,  1.,  0.,  0.],
                           [0.,  0., -1.007021, -2.253885],
                           [0.,  0., -1.,  0.]])

        assert_array_almost_equal(camera.projection_matrix, matrix)
