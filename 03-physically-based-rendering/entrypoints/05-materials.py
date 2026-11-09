import numpy as np
from OpenGL import GL
import sys
#sys.path.insert(0, r"C:\Users\rafae\2026-cg03-pbr-243360_245609\src")
#import urenderer
from urenderer.renderer.opengl import Texture

# Você deve acrescentar suporte para texturas de base color, metallic, roughness
# com tiling ao modelo de sombreamento.
#
# Altere o arquivo 05-fragment.fs

if __name__ == "__main__":
    urenderer.utils.clear_workdir("05-materials")
    renderer = urenderer.renderer.OpenGLRenderer(1920, 1080)
    renderer.background_color = np.array([0, 0, 0, 1], np.float32)
    runtime = urenderer.application.Runtime(
        renderer, name="05-materials")

    renderer.ambient_color = np.array([0.1, 0.1, 0.1], dtype=np.float32)

    shader = urenderer.renderer.Shader("vertex.vs", "05-fragment.fs")

    # Material Metálico
    metalBaseColor = Texture.load_file("materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Color.jpg",
                                       srgb=True, drop_alpha=True)
    metalMetallic = Texture.load_file(
        "materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Metalness.jpg", drop_alpha=True)
    metalRoughness = Texture.load_file(
        "materials/Metal048A_1K-JPG/Metal048A_1K-JPG_Roughness.jpg", drop_alpha=True)

    materialMetal = urenderer.renderer.opengl.Material(shader)
    materialMetal.set_texture(0, "baseColorTexture", metalBaseColor)
    materialMetal.set_texture(1, "metallicTexture", metalMetallic)
    materialMetal.set_texture(2, "roughnessTexture", metalRoughness)

    # Material semi-metálico
    materialMetal2 = materialMetal.clone()
    metalMetallic2 = Texture(
        200*np.ones((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    materialMetal2.set_texture(1, "metallicTexture", metalMetallic2)

    # Material dielétrico
    brickBaseColor = Texture.load_file("materials/Bricks104_1K-JPG/Bricks104_1K-JPG_Color.jpg",
                                       srgb=True, drop_alpha=True)
    brickMetallic = Texture(np.zeros((1, 1), np.uint8), GL.GL_RED, GL.GL_R8)
    brickRoughness = Texture.load_file(
        "materials/Bricks104_1K-JPG/Bricks104_1K-JPG_Roughness.jpg", drop_alpha=True)

    materialBrick = urenderer.renderer.opengl.Material(shader)
    materialBrick.set_texture(0, "baseColorTexture", brickBaseColor)
    materialBrick.set_texture(1, "metallicTexture", brickMetallic)
    materialBrick.set_texture(2, "roughnessTexture", brickRoughness)
    materialBrick.set_uniform("tiling", 1.0)

    # Material dielétrico com tiling
    materialBrick2 = materialBrick.clone()
    materialBrick2.set_uniform("tiling", 10.0)

    # Cria esferas utilizando os materiais
    sphere = urenderer.node.Node()
    sphere.translation = np.array([1, 0, -5], np.float64)
    sphere.render_data["mesh"] = urenderer.geometry.mesh.get_mesh_sphere()
    sphere.render_data["material"] = materialMetal
    runtime.scene.add_child(sphere)

    sphere2 = sphere.clone()
    sphere2.translation = np.array([3.5, 0, -5], np.float64)
    sphere2.render_data["material"] = materialMetal2

    sphere3 = sphere.clone()
    sphere3.translation = np.array([-1, 0, -5], np.float64)
    sphere3.render_data["material"] = materialBrick

    sphere4 = sphere.clone()
    sphere4.translation = np.array([-3.5, 0, -5], np.float64)
    sphere4.render_data["material"] = materialBrick2
    runtime.scene.add_child(sphere2)  # ← falta isso
    runtime.scene.add_child(sphere3)  # ← falta isso
    runtime.scene.add_child(sphere4)
    # Luzes
    light = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light.rotation = np.array([45, 45, 45], np.float64)
    light.light_intensity = 3.0
    runtime.scene.add_child(light)

    light = urenderer.node.Light(urenderer.node.LightType.DIRECTIONAL)
    light.rotation = np.array([-45, -45, -45], np.float64)
    light.light_intensity = 1.0
    runtime.scene.add_child(light)

    runtime.loop(capture=[1])
