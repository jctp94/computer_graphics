
# **Manual del taller 4 - FPS Geométrico en Ogre3D**

## **1. Descripción del Proyecto**
Este proyecto implementa un videojuego estilo **First-Person Shooter (FPS)** utilizando **Ogre3D** y **VTK** para la visualización de geometrías de enemigos. El juego presenta enemigos como esferas, cilindros, conos y cajas, que deben ser eliminados por el jugador, quien tiene que disparar balas desde una vista en primera persona.

---

## **2. Requisitos Previos**

Antes de comenzar, asegúrate de tener los siguientes programas instalados:

- **Python 3.12**
- **Ogre3D** (asegurate de tener la versión correcta de Ogre compatible con el sistema)
- **VTK** (para las geometrías paramétricas)
- **SDL** (para la gestión de la entrada de teclado y mouse)

---

## **3. Estructura del Proyecto**

El proyecto se organiza en varios archivos clave:

```
/src
    /GeometricFPS
        GeometricFPS.py          # Lógica principal del juego
        FPSListener.py            # Listener para manejar entradas (teclado y mouse)
        resources.cfg             # Configuración de recursos
        /resources
            all.material          # Materiales y texturas
            ball.jpg              # Textura de enemigos
            ground.jpg            # Textura del suelo
            scene.txt             # Configuración de la escena (enemigos, cámaras, etc.)
/lib
    /PUJ_Ogre
        BaseApplication.py       # Lógica base para la aplicación Ogre3D
        BaseApplicationWithVTK.py # Extiende la funcionalidad con VTK
        BaseListener.py          # Controlador de entrada base
        __init__.py              # Inicialización de la librería
```

---

## **4. Instalación**

### **4.1. Instalación de Dependencias**

1. **Ogre3D**: Descarga e instala Ogre3D desde su [sitio oficial](https://www.ogre3d.org/).
2. **VTK**: Instala VTK desde [VTK.org](https://vtk.org/).
3. **Python**: Asegúrate de tener Python 3.12 y de haber configurado el entorno correctamente.
4. **SDL**: Puedes instalar SDL a través de tu gestor de paquetes si estás en Linux, o descargarlo desde su [sitio web](https://www.libsdl.org/download-2.0.php) si usas Windows.

### **4.2. Configuración de Ogre3D en el Proyecto**

1. Asegúrate de tener configurado Ogre3D en tu entorno de desarrollo.
2. En el archivo `resources.cfg`, se definen las rutas para las texturas y materiales, asegúrate de que las rutas de las texturas sean correctas.

---

## **5. Configuración del Proyecto**

El archivo de configuración `scene.txt` contiene la información sobre los enemigos, la cámara y otros aspectos del entorno. Aquí hay un ejemplo de su contenido:

```txt
ground -200 200 -200 200
camera 1e-3 1.7 1.0
skycolor 0.7 0.5 0.9
sphere 1.0 bad_guy1 5 0.07 3
cylinder 0.3 0.5 bad_guy1 10 0.03 30
bullet 0.05 bullet_bross 5 15 1 5
```

### **Explicación de `scene.txt`:**

- **ground**: Coordenadas que definen los límites del suelo del juego.
- **camera**: Posición de la cámara inicial.
- **skycolor**: Color del fondo del cielo.
- **sphere/cylinder**: Definiciones de los enemigos, incluyendo su material, vida (stamina), probabilidad de aparición, y cantidad máxima de enemigos.
- **bullet**: Parámetros de las balas, como su material, daño, velocidad, cantidad máxima, y tiempo de vida.

---

## **6. Controles del Juego**

El juego se maneja utilizando las siguientes teclas:

- **WASD**: Movimiento del jugador en el espacio.
- **Espacio**: Salto del jugador.
- **Click del mouse**: Disparo de las balas.

---

## **7. Funcionalidades del Código**

### **7.1. Inicialización del Juego**

El juego se inicializa en el archivo `GeometricFPS.py`:

```python
def __init__( self ):
    super( GeometricFPS, self ).__init__( 'GeometricFPS v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
```

Este código configura el juego con el título y el archivo de recursos que contiene las configuraciones necesarias.

### **7.2. Movimiento del Jugador**

El movimiento del jugador se gestiona con el `CameraMan` de Ogre, que está vinculado al movimiento del ratón y las teclas WASD. Además, se maneja la posición de la cámara para que se mantenga a una altura fija.

### **7.3. Disparo de Balas**

Las balas se generan en el espacio 3D y se mueven en la dirección de la cámara:

```python
def shootBullet( self ):
    name = self.m_AvailableNames['bullet'].pop( 0 )
    node = self._createManualObject( self.m_Bullets['bullet'][ 5 ], name, self.m_Bullets['bullet'][ 0 ] )
    ...
    node.setPosition(target_pos)
    node.setOrientation(cam_orient)
    self.m_AliveBullets.append({'node': node, 'name': name, 'alive_time': 0})
```

### **7.4. Colisión de Balas con Enemigos**

Cuando una bala impacta a un enemigo, se aplica el daño y se elimina al enemigo si su salud llega a cero:

```python
for bad_guy in self.m_AliveBadGuys[bad_guy_type]:
    if bullet['node'].getPosition().distance(bad_guy['node'].getPosition()) < self.m_BadGuys[bad_guy_type][-1]:
        bad_guy['stamina'] -= self.m_Bullets['bullet'][1]
        bullets_to_remove.append(bullet)
```

## **8. Conclusión**

Este juego proporciona una buena base para un proyecto de FPS simple usando Ogre3D. Puedes extender las mecánicas agregando más tipos de enemigos, efectos visuales, y mejorando la jugabilidad.

---

## **11. Créditos**

- **Desarrolladores**: Jesús David Romero Melo, Juan Camilo Torres Peña y Jonatan Alejandro Gallo Martínez.
- **Correo**: jesus-romero@javeriana.edu.co, torrespjc@javeriana.edu.co y jonatan.gallo@javeriana.edu.co
