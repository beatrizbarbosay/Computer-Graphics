import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from urenderer.node import Camera, Node
from urenderer.renderer.renderer import Renderer

matplotlib.use("Agg")  # backend sem janela; troque por "TkAgg" se quiser exibir ao vivo


class PyplotRenderer(Renderer):
    '''
    Renderer using Matplotlib/Pyplot.

    Projects 3-D geometry onto the screen plane and draws wireframes.
    Useful for debugging without requiring an OpenGL context.
    '''

    def __init__(self, screen_width: int, screen_height: int) -> None:
        '''
        PyplotRenderer initializer.

        Args:
            screen_width (int): screen width in pixels
            screen_height (int): screen height in pixels
        '''
        super().__init__(screen_width, screen_height)

        self.background_color = np.array([0.0, 0.0, 0.0, 1.0], np.float32)
        self._name = "PyplotRenderer"

        # Cria a figura com o tamanho pedido (polegadas × dpi = pixels)
        dpi = 100
        self._dpi = dpi
        self._fig, self._ax = plt.subplots(
            figsize=(screen_width / dpi, screen_height / dpi),
            dpi=dpi
        )

        self._view_matrix: np.ndarray = np.eye(4)
        self._projection_matrix: np.ndarray = np.eye(4)

        # Lista de primitivas acumuladas no frame atual: [(xs, ys, color), ...]
        self._lines: list[tuple[list, list, str]] = []

    # ------------------------------------------------------------------
    # Interface Renderer
    # ------------------------------------------------------------------

    def start(self, camera: Camera, view_matrix: np.ndarray, name: str) -> None:
        '''
        Start the frame rendering — clear the axes and store matrices.
        '''
        self._view_matrix = view_matrix
        self._projection_matrix = camera.projection_matrix
        self._name = name

        self._lines = []

        self._ax.clear()

        bg = self.background_color[:3]
        self._fig.patch.set_facecolor(bg)
        self._ax.set_facecolor(bg)

        self._ax.set_xlim(-1, 1)
        self._ax.set_ylim(-1, 1)
        self._ax.set_aspect("equal")
        self._ax.axis("off")

    def validate(self, node: Node) -> bool:
        '''
        Validates a node: needs a mesh in render_data.
        '''
        return "mesh" in node.render_data

    def render_valid_node(self, node: Node, model_transformation: np.ndarray) -> None:
        '''
        Projects the mesh vertices and draws triangle wireframes.
        '''
        mesh = node.render_data["mesh"]

        vertices: np.ndarray = mesh.vertex.reshape(-1, 3)   # (N, 3)
        indices: np.ndarray  = mesh.index.reshape(-1, 3)    # (T, 3)

        # MVP: model → world → view → clip
        mvp = self._projection_matrix @ self._view_matrix @ model_transformation

        # Homogeneous coordinates (N, 4)
        ones = np.ones((len(vertices), 1), dtype=np.float32)
        verts_h = np.hstack([vertices.astype(np.float32), ones])  # (N, 4)

        # Transform
        clip = (mvp @ verts_h.T).T  # (N, 4)

        # Perspective divide → NDC
        w = clip[:, 3:4]
        w = np.where(np.abs(w) < 1e-6, 1e-6, w)   # evita divisão por zero
        ndc = clip[:, :2] / w                       # (N, 2)  x,y em [-1, 1]

        # Escolhe cor do wireframe
        color = "white" if np.mean(self.background_color[:3]) < 0.5 else "black"
        if "material" in node.render_data:
            mat = node.render_data["material"]
            if hasattr(mat, "color"):
                color = mat.color

        # Desenha cada triângulo
        for tri in indices:
            i0, i1, i2 = tri
            xs = [ndc[i0, 0], ndc[i1, 0], ndc[i2, 0], ndc[i0, 0]]
            ys = [ndc[i0, 1], ndc[i1, 1], ndc[i2, 1], ndc[i0, 1]]
            self._ax.plot(xs, ys, color=color, linewidth=0.5)

    def end(self, capture: bool = False) -> None:
        '''
        Finalizes the frame — optionally saves to disk and shows the plot.
        '''
        self._ax.set_title(self._name, color="white", fontsize=8)
        self._fig.tight_layout(pad=0)

        if capture:
            from urenderer.utils import get_filename_unique
            filename = get_filename_unique(self._name)
            self._fig.savefig(filename, dpi=self._dpi,
                              facecolor=self._fig.get_facecolor())

        # Para exibir ao vivo troque o backend para TkAgg/Qt5Agg e descomente:
        # plt.pause(0.001)

    def should_stop(self) -> bool:
        return False