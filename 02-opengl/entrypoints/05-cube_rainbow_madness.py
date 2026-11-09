
import numpy as np
import urenderer
from OpenGL import GL
from urenderer.node import Node


def update_cube(node: Node, deltaTime: float, time_since_start: float) -> None:
    material: urenderer.renderer.opengl.Material = node.render_data["material"]

    ## SEU CÓDIGO AQUI ######################################################
    material.set_uniform("time", float(time_since_start))

    #########################################################################

    time_since_start /= 10
    t = time_since_start - int(time_since_start)

    node.rotation[0] = 45
    node.rotation[1] = 360*t
    node.rotation[2] = 0


if __name__ == "__main__":
    urenderer.utils.clear_workdir("05-cube_raindow_madness")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1.0])
    runtime = urenderer.application.Runtime(
        renderer, name="05-cube_raindow_madness")

    shader = urenderer.renderer.Shader(
        "05-vertex.vs", "05-fragment.fs")
    material = urenderer.renderer.opengl.Material(shader)

   ## SEU CÓDIGO AQUI ######################################################
    cube_mesh = urenderer.geometry.mesh.get_mesh_cube()

    quantidade_de_cubos = 50
    
    for i in range(quantidade_de_cubos):
        cubo = urenderer.node.Node()
        cubo.callbacks.append(update_cube)
        cubo.render_data["mesh"] = cube_mesh
        cubo.render_data["material"] = material
        
        # X e Y variam entre -10 e 10. Z vai para o fundo (entre -25 e -5)
        pos_x = np.random.uniform(-10.0, 10.0)
        pos_y = np.random.uniform(-10.0, 10.0)
        pos_z = np.random.uniform(-25.0, -5.0)
        cubo.translation = np.array([pos_x, pos_y, pos_z], np.float64)
        
        escala = np.random.uniform(0.5, 2.5)
        cubo.scale = np.array([escala, escala, escala], np.float64)
        
        runtime.scene.add_child(cubo)

    #########################################################################

    runtime.loop(n=4000, capture=np.arange(0, 4000, 40, dtype=np.int32))
    urenderer.utils.image_to_video("05-cube_raindow_madness", fps=30)
    urenderer.utils.clear_workdir("05-cube_raindow_madness", image_only=True)
