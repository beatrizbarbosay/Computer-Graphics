import numpy as np
import urenderer

# Renderiza um cubo branco utilizando o OpenGL renderer.
#
# Você precisa escrever o shader 01-vertex.vs para realizar a transformação de coordenadas (model -> world -> view -> projection )
# e 01-fragment.fs para definir as cores dos fragmentos

if __name__ == "__main__":
    urenderer.utils.clear_workdir("01-hello_cube")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(renderer, name="01-hello_cube")

    shader = urenderer.renderer.Shader("01-vertex.vs", "01-fragment.fs")
    material = urenderer.renderer.opengl.Material(shader)

    cube = urenderer.node.Node()

    cube.translation = np.array([0, 0, -5], np.float64)
    cube.rotation = np.array([45, 45, 45], np.float64)
    cube.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_cube()
    cube.render_data["material"] = material
    runtime.scene.add_child(cube)
    runtime.camera.screen_width = 1920
    runtime.camera.screen_height = 1080
    print("view:\n", runtime._view_matrix)
    print("proj:\n", runtime.camera.projection_matrix)
    runtime.loop(capture=[0])
