import numpy as np
import urenderer

# Renderize 1 triângulo com vertex colors
# A cor final dos fragmentos deve ser a interpolação das cores dos vértices

if __name__ == "__main__":
    urenderer.utils.clear_workdir("04-colors")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(renderer, name="04-colors")

    shader = urenderer.renderer.Shader(
        "04-vertex.vs", "04-fragment.fs")
    material = urenderer.renderer.opengl.Material(shader)

    node = urenderer.node.Node()

    node.translation = np.array([0, 0, -2], np.float64)
    node.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_triangle()
    node.render_data["material"] = material

## SEU CÓDIGO AQUI ######################################################
    
    #cores no formato RGB
    cores = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)

    node.render_data["mesh"].color = cores

    #########################################################################

    runtime.scene.add_child(node)

    runtime.loop(capture=[0])
