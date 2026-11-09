#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 2) in vec3 aColor; // Captura a cor com "a" minúsculo e "C" maiúsculo


uniform mat4 modelTransformation;
uniform mat4 viewTransformation;
uniform mat4 projectionMatrix;

out vec3 Color;

void main()
{
    gl_Position = projectionMatrix * viewTransformation * modelTransformation * vec4(aPos, 1.0);
    

    Color = aColor;
}