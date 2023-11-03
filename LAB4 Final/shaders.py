# En OpenGL, los shaders se escriben en un nuevo lenguaje de programacion llamada GLSL
# Graphics Library Shader Language

vertex_shader = '''
# version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 UVs;
out vec3 outNormals;
out vec3 outPosition;

void main()
{
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(position,1.0);
    UVs = texCoords;
    outNormals = (modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    outPosition = position;
}
'''

fat_vertex_shader = '''
#version 450 core
layout (location=0) in vec3 position;
layout (location=1) in vec2 texCoords;
layout (location=2) in vec3 normals;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float fatness;

out vec2 UVs;
out vec3 outNormals;

void main()
{
    outNormals  =(modelMatrix*vec4(normals,0.0)).xyz;
    outNormals = normalize(outNormals);
    vec3 pos = position+(fatness/4)*outNormals;
    
    gl_Position = projectionMatrix*viewMatrix*modelMatrix*vec4(pos,1.0);
    UVs = texCoords;
}
'''

toon_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    if (intensity<0.33)
        intensity=0.2;
    else if (intensity<0.66)
        intensity=0.6;
    else
        intensity=1.0;
    fragColor = texture(tex,UVs)*intensity;
}

'''

gourad_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform vec3 dirLight;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    float intensity = dot(outNormals,-dirLight);
    fragColor = texture(tex,UVs)*intensity;
}

'''

unlit_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

in vec2 UVs;
in vec3 outNormals;

out vec4 fragColor;

void main()
{
    fragColor = texture(tex,UVs);
}

'''

wave_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;
uniform mat4 modelMatrix;

in vec2 UVs;
in vec3 outNormals;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    vec3 rotatedPosition = (modelMatrix * vec4(outPosition, 1.0)).xyz;
    vec2 uv = UVs;
    uv.y += sin(uv.x * 10.0 + rotatedPosition.x + time) * 0.1;
    fragColor = texture(tex, uv);
}

'''

checkerbord_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform mat4 modelMatrix;

in vec2 UVs;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    vec3 rotatedPosition = (modelMatrix * vec4(outPosition, 1.0)).xyz;
    vec2 uv = UVs * 10.0 + rotatedPosition.xz; // Rotate based on object position
    float checker = mod(floor(uv.x) + floor(uv.y), 2.0);
    checker = checker * 0.8 + 0.2; // Adjust brightness
    fragColor = vec4(checker, checker, checker, 1.0) * texture(tex, UVs);
}



'''

ripple_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;
uniform mat4 modelMatrix;

in vec2 UVs;
in vec3 outPosition;

out vec4 fragColor;

void main()
{
    vec3 rotatedPosition = (modelMatrix * vec4(outPosition, 1.0)).xyz;
    vec2 uv = UVs;
    float dist = distance(uv, vec2(0.5, 0.5));
    uv += sin(dist * 10.0 - time * 5.0 + rotatedPosition.x) * 0.01;
    fragColor = texture(tex, uv);
}


'''

noise_shader = '''
#version 450 core

layout (binding=0) uniform sampler2D tex;

uniform float time;
uniform mat4 modelMatrix;

in vec2 UVs;
in vec3 outPosition;

out vec4 fragColor;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main()
{
    vec3 rotatedPosition = (modelMatrix * vec4(outPosition, 1.0)).xyz;
    vec2 uv = UVs;
    float noise = random(uv * time + rotatedPosition.xy);
    fragColor = texture(tex, uv) * noise;
}

'''