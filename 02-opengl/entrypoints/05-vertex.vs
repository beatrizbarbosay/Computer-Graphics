#version 330 core
// Utilize as transformações de coordenadas do 01-vertex.vs
//
// A cor de cada vértice precisa ser HSV(h, 1, 1), em que 
// o hue h varia entre 0 e 1 a partir do tempo.
//
// Utilize a UV do vértice para variar a posição de início
// do h: h = f(time)+g(uv), f e g são operações definidas por você
//
// Observe que a cor de saída precisa estar em RGB

layout(location = 0) in vec3 aPos;
layout(location = 1) in vec2 uv;

out vec3 LocalPos;
out vec3 color;

uniform mat4 modelTransformation;
uniform mat4 viewTransformation;
uniform mat4 projectionMatrix;

uniform float time;

/// Converte uma cor de HSV para RGB
vec3 hsv2rgb(vec3 hsv)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(hsv.xxx + K.xyz) * 6.0 - K.www);
    return hsv.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), hsv.y);
}

/// Converte uma cor de RGB para HSV
vec3 rgb2hsv(vec3 color)
{
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(color.bg, K.wz), vec4(color.gb, K.xy), step(color.b, color.g));
    vec4 q = mix(vec4(p.xyw, color.r), vec4(color.r, p.yzx), step(p.x, color.r));

    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

/// Gera um valor pseudo-aleatório a partir da UV
float random(vec2 st)
{
    return fract(sin(dot(st.xy, vec2(12.9898, 78.233))) * 43758.5453123);
}

void main()
{
    gl_Position = projectionMatrix * viewTransformation * modelTransformation * vec4(aPos, 1.0);
    LocalPos = aPos;

    float hue = (sin(time) + 1) / 2;
    hue += mix(-2.0, 2.0, random(uv));

    // Pega apenas a parte decimal do hue
    hue = fract(hue);

    vec3 hsv = vec3(hue, 1, 1);
    color = hsv2rgb(hsv);
}