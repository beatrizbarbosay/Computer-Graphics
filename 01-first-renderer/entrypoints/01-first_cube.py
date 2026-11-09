import numpy as np
import urenderer

# Cria uma cena com um cubo e renderiza ela utilizando o PyplotRenderer

if __name__ == "__main__":
    urenderer.utils.clear_workdir("01-first_cube")
    renderer = urenderer.renderer.PyplotRenderer(1920, 1080)
    runtime = urenderer.application.Runtime(renderer, name="01-first_cube")

    cube = urenderer.node.Node()

    cube.translation = np.array([0, 0, -5], np.float64)
    cube.rotation = np.array([45, 45, 45], np.float64)
    cube.render_data = urenderer.geometry.polygonal_ifs.get_ifs_cube()

    runtime.scene.add_child(cube)

    runtime.iter(capture=True)
