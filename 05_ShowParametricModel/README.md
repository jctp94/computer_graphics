# ShowParametricModel

## 🎯 Objetivo del Proyecto
Implementar un programa en **C++** que demuestre el concepto de **bump mapping** para visualizar **superficies paramétricas 3D** con relieve simulado.  
El programa recibe por línea de comandos un archivo de imagen **PPM (Netpbm)** y asigna normales a un modelo paramétrico basadas en los colores de la imagen, utilizando ecuaciones paramétricas en parámetros *u* y *v*.  

Esto permite entender:
- Mapeo de texturas y normales.
- Uso de fuentes de luz y materiales en **OpenGL**.
- Visualización realista de superficies 3D.

El resultado esperado es la visualización de superficies paramétricas (plano, esfera, cilindro, superficie ondulada) con **iluminación realista** donde:
- La textura PPM actúa como mapa difuso.
- Las normales calculadas vía derivadas parciales (*du* y *dv*) crean el efecto de **relieve simulado** sin modificar la geometría.

---

## 🛠️ Descripción Técnica

### Entrada
- Archivo **PPM** (ejemplo: `texture.ppm`) usado para textura y mapeo de normales.

### Modelos Soportados
- **Plano base:** u,v en [-1, 1].
- **Esfera:** u ∈ [0, 2π], v ∈ [0, π].
- **Cilindro:** u ∈ [0, 2π], v ∈ [-1, 1].
- **Superficie ondulada:** plano con ondas sinusoidales en Z (bump procedural).

### Funcionalidades Clave
- **Bump Mapping:** cálculo de normales como `du × dv` en `ParametricModel::build()`.
- **Ecuaciones paramétricas:** definidas en `App.cxx` (punto, du, dv).
- **Iluminación:** luz direccional fija (`GL_LIGHT0`), ambiente/difuso/especular.
- **Materiales:** configurables vía `glMaterialfv`. El difuso se sobrescribe con la textura PPM.
- **Renderizado:** sombreado suave, `GL_DEPTH_TEST`, texturas por vértice, sin *culling* (ambas caras visibles).
- **Cámara:** tipo *trackball* (`PUJ_GL::TrackballCamera`) con zoom, rotación y reset.
- **Resolución:** hasta **175x175 muestras (~60k triángulos)** para detalles finos.
- **Lenguaje y bibliotecas:**  
  - C++  
  - OpenGL/GLUT  
  - Eigen3 (álgebra lineal)  
  - CMake (build system)  
  - Biblioteca personalizada **PUJ_GL**

---

## 💻 Requisitos del Proyecto

### Hardware/Software
- **SO:** Linux (probado en Ubuntu/Debian).
- **Compilador:** GCC/G++ 13.3.0+.
- **RAM mínima:** 4 GB (soporta ~100k triángulos).

### Herramientas
- CMake 3.11+  
- Make (gmake)  

### Bibliotecas
Instalar con:
```bash
sudo apt install freeglut3-dev libgl1-mesa-dev libglu1-mesa-dev libeigen3-dev
```

---
## 📁 Estructura del proyecto
```
05_ShowParametricModel/
│
├─ lib/PUJ_GL/ # Librería base para gráficos y escena
│ ├─ BaseApp.* # Clase base de la aplicación
│ ├─ Camera.* # Cámara y control de vista
│ ├─ Mesh.* # Estructura y carga de mallas
│ ├─ ParametricModel.* # Implementación del modelo paramétrico
│ ├─ Scene.* # Manejo de la escena
│ └─ ...
│
├─ meshes/ # Modelos 3D de ejemplo (.obj)
│ ├─ bunny.obj
│ ├─ cube.obj
│ ├─ ship.obj
│ └─ texture.ppm
│
├─ App.cxx / App.h # Lógica principal de la aplicación
├─ main.cxx # Punto de entrada del programa
├─ CMakeLists.txt # Configuración del proyecto con CMake
└─ README.md # Documentación
```

---
## rear carpeta de compilación:
```bash
mkdir build && cd build
```

## Configurar con CMake:
```bash
cmake ..
```

## Compilar el proyecto:
```bash
make
```

## Ejecutar la aplicación:
```bash
./PUJ_GL_ShowParametricModel ../meshes/texture.ppm
```