import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

import urenderer


class TestNode(unittest.TestCase):
    def test_scale(self) -> None:
        node = urenderer.node.Node()
        node.scale = np.array([1.0, -2.0, 3.0])

        matrix = np.array([[1.0, 0.0, 0.0, 0.0],
                           [0.0, -2.0, 0.0, 0.0],
                           [0.0, 0.0, 3.0, 0.0],
                           [0.0, 0.0, 0.0, 1.0]])
        assert_array_almost_equal(node.model_transform, matrix)

    def test_translation(self) -> None:
        node = urenderer.node.Node()
        node.translation = np.array([1.0, -2.0, 3.0])

        matrix = np.array([[1.0, 0.0, 0.0, 1.0],
                           [0.0, 1.0, 0.0, -2.0],
                           [0.0, 0.0, 1.0, 3.0],
                           [0.0, 0.0, 0.0, 1.0]])
        assert_array_almost_equal(node.model_transform, matrix)

    def test_rotation(self) -> None:
        node = urenderer.node.Node()
        node.rotation = np.array([-45.0, 15.5, 0.0])

        matrix = np.array(([[0.96363045, -0.18896607,  0.18896607, 0.0],
                            [0.,  0.70710678,  0.70710678, 0.0],
                            [-0.26723838, -0.68138963,  0.68138963, 0.0],
                            [0.0, 0.0, 0.0, 1.0]]))
        assert_array_almost_equal(node.model_transform, matrix)

    def test_composition(self) -> None:
        node = urenderer.node.Node()
        node.scale = np.array([1.0, -2.0, 3.0])
        node.translation = np.array([1.0, -2.0, 3.0])
        node.rotation = np.array([-45.0, 15.5, 0.0])

        matrix = np.array([[0.96363045,  0.37793214,  0.5668982,  1.0],
                           [0., -1.41421356,  2.12132034,  -2.0],
                           [-0.26723838,  1.36277926,  2.04416888,  3.0],
                           [0.,  0.,  0.,  1.]])

        assert_array_almost_equal(node.model_transform, matrix)
