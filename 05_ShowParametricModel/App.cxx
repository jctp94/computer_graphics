// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include "App.h"
#include <PUJ_GL/Image.h>
#include <PUJ_GL/Traits.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <cmath>
#include <iostream> // Para depuración

// -------------------------------------------------------------------------
// Modified parametric_model function to return partial derivatives
void parametric_model(
  PUJ_GL::Traits::TReal* point, PUJ_GL::Traits::TReal* normal,
  PUJ_GL::Traits::TReal* du, PUJ_GL::Traits::TReal* dv,
  const PUJ_GL::Traits::TReal& u, const PUJ_GL::Traits::TReal& v
  )
{
  // Example: A simple plane for demonstration - ESCALA AUMENTADA para visibilidad
  PUJ_GL::Traits::TReal scale = 1.0f;
  PUJ_GL::Traits::TReal amplitude = 0.1f; // Amplitud de la onda
  PUJ_GL::Traits::TReal frequency = 5.0f; // Frecuencia de la onda
  point[0] = scale * u;
  point[1] = scale * v;
  point[2] = amplitude * std::sin(frequency * u) * std::cos(frequency * v);
  // Derivadas parciales
  du[0] = scale;
  du[1] = 0.0f;
  du[2] = amplitude * frequency * std::cos(frequency * u) * std::cos(frequency * v);
  dv[0] = 0.0f;
  dv[1] = scale;
  dv[2] = -amplitude * frequency * std::sin(frequency * u) * std::sin(frequency * v);

  // La normal aquí no se usa directamente para el renderizado final,
  // pero se pasa para mantener la firma. La normal real se calcula
  // en ParametricModel::build usando du y dv.
  normal[0] = 0.0f; 
  normal[1] = 0.0f; 
  normal[2] = 1.0f;
}


// -------------------------------------------------------------------------
App::
App(
  int* argc, char** argv,
  int w, int h,
  int x, int y
  )
  : Superclass(
    argc, argv, GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH, w, h, x, y, "Show a parametric model"
    )
{
  PUJ_GL::Image* image = nullptr;
  if( *argc > 1 )
  {
    image = new PUJ_GL::Image( );
    if( !( image->read_from_Netpbm( argv[ 1 ] ) ) )
    {
      delete image;
      image = nullptr;
      std::cerr << "Error reading image file: " << argv[ 1 ] << std::endl;
    } // end if
  } // end if
  this->m_Scene.load_parametric_model(
    parametric_model,
    1.0f, -1.0f, 180, false, 
    1.0f, -1.0f, 180, false,
    image
  );

  // Setear materiales usando get_last_object
  auto* last_obj = this->m_Scene.get_last_object();
  if (last_obj) {
    PUJ_GL::Mesh* mesh = last_obj->m_Mesh; // Acceso directo si m_Mesh es público
    if (mesh) {
      mesh->set_material_ambient(0.2f, 0.2f, 0.2f);
      mesh->set_material_diffuse(0.8f, 0.8f, 0.8f);
      mesh->set_material_specular(1.0f, 1.0f, 1.0f);
      mesh->set_material_shininess(50.0f);
    }
  }

  // Configurar la cámara al bounding box de la escena
  this->m_Camera.configure( this->m_Scene.bounding_box( ) );
  this->m_Camera.reset();  // Forzar reset para ajustar vista inicial al modelo

  // Cargar base ortogonal para ejes de referencia (opcional)
  this->m_Scene.load_orthobase( 0.1 );
}

// -------------------------------------------------------------------------
App::
~App( )
{
}

// -------------------------------------------------------------------------
void App::
init( )
{
  this->Superclass::init( );
  const TReal* c = this->m_Scene.clear_color( );
  glClearColor( c[ 0 ], c[ 1 ], c[ 2 ], c[ 3 ] );
  glEnable( GL_DEPTH_TEST ); // Habilitar prueba de profundidad
  glEnable( GL_LIGHTING );   // Habilitar iluminación
  glEnable( GL_LIGHT0 );     // Habilitar la luz 0
  glShadeModel( GL_SMOOTH ); // Sombreado suave

  // Configurar propiedades de la luz
  GLfloat light_ambient[] = { 0.2f, 0.2f, 0.2f, 1.0f };
  GLfloat light_diffuse[] = { 1.0f, 1.0f, 1.0f, 1.0f };
  GLfloat light_specular[] = { 1.0f, 1.0f, 1.0f, 1.0f };
  // Posición inicial de la luz: direccional desde (1,1,1) - se actualizará en display
  GLfloat light_position[] = { 5.0f, 5.0f, 5.0f, 0.0f };  // Ajustado para el nuevo tamaño

  glLightfv( GL_LIGHT0, GL_AMBIENT, light_ambient );
  glLightfv( GL_LIGHT0, GL_DIFFUSE, light_diffuse );
  glLightfv( GL_LIGHT0, GL_SPECULAR, light_specular );
  glLightfv( GL_LIGHT0, GL_POSITION, light_position );

  // Resetear cámara después de init para asegurar visibilidad
  this->m_Camera.reset();
  std::cout << "Inicialización completada. Cámara reseteada." << std::endl;
}

// -------------------------------------------------------------------------
void App::
_cb_reshape( int width, int height )
{
  TReal a = 1.0;

  if( height != 0 )
    a = TReal( width ) / TReal( height );

  glViewport( 0, 0, width, height );

  glMatrixMode( GL_PROJECTION );
  glLoadIdentity( );

  this->m_Camera.load_perspective( a );

  glutPostRedisplay( );
}

// -------------------------------------------------------------------------
void App::
_cb_display( )
{
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );  // Limpiar buffers
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  this->m_Camera.look( );  // Aplicar transformación de la cámara

  // Ubicar la luz relativa a la cámara (con offset para evitar coincidencia con origen)
  GLfloat light_position[] = { 0.0f, 0.0f, 1.0f, 1.0f };  // Luz posicional ligeramente elevada
  glLightfv( GL_LIGHT0, GL_POSITION, light_position );

  this->m_Scene.draw( );  // Dibujar la escena
  
  glutSwapBuffers( );
}
// -------------------------------------------------------------------------
void App::
_cb_mouse( int button, int state, int x, int y )
{
  if( state == 1 && ( button == 3 || button == 4 ) )
  {
    this->m_Camera.zoom( 1e-1 * TReal( ( button == 3 )? -1: 1 ) );
    glutPostRedisplay( );
  } // end if
}

// -------------------------------------------------------------------------
void App::
_cb_special( int key, int x, int y )
{
  static const TReal a = std::atan( TReal( 1 ) ) / TReal( 45 );

  if( key == 100 ) // Left
  {
    this->m_Camera.yaw( -a );
    glutPostRedisplay( );
  }
  else if( key == 102 ) // Right
  {
    this->m_Camera.yaw( a );
    glutPostRedisplay( );
  }
  else if( key == 101 ) // Up
  {
    this->m_Camera.pitch( -a );
    glutPostRedisplay( );
  }
  else if( key == 103 ) // Down
  {
    this->m_Camera.pitch( a );
    glutPostRedisplay( );
  } // end if
}

// -------------------------------------------------------------------------
void App::
_cb_keyboard( unsigned char key, int x, int y )
{
  if( key == 'r' || key == 'R' )
  {
    this->m_Camera.reset( );
    glutPostRedisplay( );
  } // end if
}

// eof - App.cxx