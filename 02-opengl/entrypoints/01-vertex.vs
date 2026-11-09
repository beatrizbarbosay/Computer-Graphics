#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aUV;
layout (location = 2) in vec3 aColor;
layout (location = 3) in vec3 aNormal;

uniform mat4 modelTransformation;
uniform mat4 viewTransformation;
uniform mat4 projectionMatrix;

out vec2 UV;
out vec3 Color;
out vec3 Normal;

void main()
{
    // Calcula a posição do vértice na tela
    gl_Position = projectionMatrix * viewTransformation * modelTransformation * vec4(aPos, 1.0);

    // Repassa os dados para o rasterizador fazer a interpolação até o Fragment Shader
    UV     = aUV;
    Color  = aColor;
    
    // Calcula a "Matriz Normal" para iluminação correta
    Normal = mat3(transpose(inverse(modelTransformation))) * aNormal;
}