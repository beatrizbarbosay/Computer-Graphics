
import numpy as np
import urenderer
from urenderer.node import Node

# Renderiza um cubo com a textura "textures/baboon.png"
#
# Altere a main para renderizar o cubo, e altere os shaders para utilizar a textura
# Verifique o funcionamento até este ponto.
#
# Corrija a função urenderer.geometry.mesh.get_mesh_cube para obter um cubo correto


def rotate(node: Node, deltaTime: float, time_since_start: float) -> None:
    time_since_start /= 10
    t = time_since_start - int(time_since_start)

    node.rotation[1] = 360*t


if __name__ == "__main__":
    urenderer.utils.clear_workdir("02-cube_texture")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="02-cube_texture")

    shader = urenderer.renderer.Shader("02-vertex.vs", "02-fragment.fs")
    material = urenderer.renderer.opengl.Material(shader)

## SEU CÓDIGO AQUI ######################################################
    
    baboon_texture = urenderer.renderer.opengl.Texture.load_file("textures/baboon.png")
    
    material.set_texture(0, "texture0", baboon_texture)
    
    #########################################################################
    cube = urenderer.node.Node()
    cube.callbacks.append(rotate)

    cube.translation = np.array([0, 0, -5], np.float64)
    cube.rotation = np.array([45, 0, 0], np.float64)
    cube.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_cube()
    cube.render_data["material"] = material

    runtime.scene.add_child(cube)

    runtime.loop(n=4000, capture=np.arange(0, 4000, 40, dtype=np.int32))
    urenderer.utils.image_to_video("02-cube_texture", fps=30)
    urenderer.utils.clear_workdir("02-cube_texture", image_only=True)
