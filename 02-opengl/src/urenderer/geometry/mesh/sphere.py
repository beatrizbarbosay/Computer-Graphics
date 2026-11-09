import numpy as np
from icosphere import icosphere

from .mesh import Mesh


def get_mesh_sphere() -> Mesh:
    '''
    Creates a icosphere in Mesh representation

    Returns:
        Mesh: icosphere mesh
    '''
    vertices, faces = icosphere(5)

    vertices = vertices.astype(np.float32)
    faces = faces.astype(np.uint32)

    uv = np.empty([vertices.shape[0], 2], dtype=np.float32)

    for i in range(vertices.shape[0]):
        x = vertices[i, 0]
        y = vertices[i, 0]
        z = vertices[i, 0]

        u = 0.5 + np.atan2(z, x) / (2*np.pi)
        v = 0.5 - np.asin(y) / np.pi

        uv[i, 0] = u
        uv[i, 1] = v

    return Mesh(vertices, faces, uv)
