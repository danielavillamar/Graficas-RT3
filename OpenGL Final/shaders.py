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

  void main()
  {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position,1.0);
    UVs = texCoords;
    outNormals = normals;
  }
'''

fragment_shader = '''
  #version 450 core

  layout (binding=0) uniform sampler2D tex;

  in vec2 UVs;
  in vec3 outNormals;

  out vec4 fragColor;

  void main()
  {
    fragColor = texture(tex, UVs);
  }

'''