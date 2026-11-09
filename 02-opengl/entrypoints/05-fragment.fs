#version 330 core

// Receba a cor do vertex e defina como cor de saída do fragmento

in vec3 color; 

out vec4 FragColor;

void main()
{
    FragColor = vec4(color, 1.0);
}