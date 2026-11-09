#version 330 core

// Utilize como base o 01-vertex.vs
// Adicione o input da UV na location=1, e crie uma nova saída para fornecer a UV ao fragment


layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aUV;
layout (location = 2) in vec3 aColor;
layout (location = 3) in vec3 aNormal;

uniform mat4 modelTransformation;
uniform mat4 viewTransformation;
uniform mat4 projectionMatrix;

out vec2 UV;

void main()
{
    gl_Position = projectionMatrix * viewTransformation * modelTransformation * vec4(aPos, 1.0);
    
    // Repassa as coordenadas de textura para o Fragment Shader
    UV = aUV;
}