// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================


#include "App.h"
#include <PUJ_GL/Image.h>
#include <PUJ_GL/Traits.h>
#include <PUJ_GL/MeshObject.h>
#include <PUJ_GL/Mesh.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <cmath>
#include <iostream> // Para depuración

// -------------------------------------------------------------------------
void parametric_model(
  PUJ_GL::Traits::TReal* point, PUJ_GL::Traits::TReal* normal,
  PUJ_GL::Traits::TReal* du, PUJ_GL::Traits::TReal* dv,
  const PUJ_GL::Traits::TReal& u, const PUJ_GL::Traits::TReal& v
  )
// {
//   // point[ 0 ] = u;
//   // point[ 1 ] = v;
//   // point[ 2 ] = 0;

//   // normal[ 0 ] = 0;
//   // normal[ 1 ] = 0;
//   // normal[ 2 ] = 1;

//   PUJ_GL::Traits::TReal radius = 1.0f; // Puedes ajustar el radio
//   point[0] = radius * std::sin(v) * std::cos(u);
//   point[1] = radius * std::sin(v) * std::sin(u);
//   point[2] = radius * std::cos(v);
//   // Derivadas parciales
//   du[0] = -radius * std::sin(v) * std::sin(u);
//   du[1] =  radius * std::sin(v) * std::cos(u);
//   du[2] =  0.0f;
//   dv[0] =  radius * std::cos(v) * std::cos(u);
//   dv[1] =  radius * std::cos(v) * std::sin(u);
//   dv[2] = -radius * std::sin(v); 

//   // PUJ_GL::Traits::TReal scale = 1.0f;
//   // PUJ_GL::Traits::TReal amplitude = 0.1f; // Amplitud de la onda
//   // PUJ_GL::Traits::TReal frequency = 5.0f; // Frecuencia de la onda
//   // point[0] = scale * u;
//   // point[1] = scale * v;
//   // point[2] = amplitude * std::sin(frequency * u) * std::cos(frequency * v);

//   normal[0] = 0.0f; 
//   normal[1] = 0.0f; 
//   normal[2] = 1.0f;

//   // normal[0] = std::sin(v) * std::cos(u); 
//   // normal[1] = std::sin(v) * std::sin(u); 
//   // normal[2] = std::cos(v);
// }

{
  //Copa ejemplo de clase
  const PUJ_GL::Traits::TReal sqrt3 = std::sqrt(3.0f);
  PUJ_GL::Traits::TReal A = sqrt3 + std::sin(v);
  PUJ_GL::Traits::TReal B = sqrt3 + std::cos(2.0f * v);
  PUJ_GL::Traits::TReal A_prime = std::cos(v);
  PUJ_GL::Traits::TReal scale = 0.2f; 
  // Puntos

  point[0] = scale * (std::cos(u) / A);
  point[1] = scale * (std::sin(u) / A);
  point[2] = scale * (v / B);

  // Derivada parcial respecto a u
  du[0] = scale * (-std::sin(u) / A);
  du[1] = scale * ( std::cos(u) / A);
  du[2] = 0.0f;

  // Derivada parcial respecto a v
  PUJ_GL::Traits::TReal B_prime = -2.0f * std::sin(2.0f * v);
  dv[0] = scale * (-std::cos(u) * A_prime / (A * A));
  dv[1] = scale * (-std::sin(u) * A_prime / (A * A));
  dv[2] = scale * ((B + 2.0f * v * std::sin(2.0f * v)) / (B * B));

  // Normal 
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
    } // end if
  } // end if

  this->m_Scene.load_parametric_model(
    parametric_model,
    //0., 2.0f * M_PI, 180, false, 0.0f, M_PI, 180, false,
    -M_PI, M_PI, 180, false, -M_PI, M_PI, 180, false, // u: -π a π, no cerrado, v: -π a π, no cerrado copa
    image
    );

  this->m_Camera.configure( this->m_Scene.bounding_box( ) );
  this->m_Scene.load_orthobase( 0.1 );
}

// -------------------------------------------------------------------------
App::
~App( )
{
}

// -------------------------------------------------------------------------
void App::init()
{
  // Inicialización base
  this->Superclass::init();

  // Color de fondo de la escena
  const TReal* c = this->m_Scene.clear_color();
  glClearColor(c[0], c[1], c[2], c[3]);

  // Buffer y z-buffer
  glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
  glEnable(GL_DEPTH_TEST);
  glDepthFunc(GL_LESS);
  glClearDepth(1.0f);

  // Luz y shading
  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);

  glEnable(GL_COLOR_MATERIAL);
  glShadeModel(GL_SMOOTH);
  glEnable(GL_NORMALIZE);
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
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );
  
  this->m_Camera.look();
  
  GLfloat light_position[] = {10.0f, 2.0f, 1.0f, 2.0f}; 
  glLightfv(GL_LIGHT0, GL_POSITION, light_position);

  GLfloat L_dif[] = {1.0f, 0.5f, 0.5f, 1.0f}; 
  glLightfv(GL_LIGHT0, GL_DIFFUSE, L_dif); 


  this->m_Scene.draw();
  glutSwapBuffers();
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
  }
  else if( key == '0' )
  {
    // Set SILVER material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(0); // SILVER
        }
      }
    }
    glutPostRedisplay( );
  }
  else if( key == '1' )
  {
    // Set SUPER_SHINY material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(1); // SUPER_SHINY
        }
      }
    }
    glutPostRedisplay( );
  }
  else if( key == '2' )
  {
    // Set SUPER_MATTE material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(2); // SUPER_MATTE
        }
      }
    }
    glutPostRedisplay( );
  } // end if
  else if( key == '3' )
  {
    // Set TEXTURED_GOLD material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(3); // TEXTURED_GOLD
        }
      }
    }
    glutPostRedisplay( );
  } // end if
  else if( key == '4' )
  {
    // Set TINT_GOLD material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(4); // TINT_GOLD
        }
      }
    }
    glutPostRedisplay( );
  } // end if
  else if( key == '5' )
  {
    // Set TEXTURED_GOLD_STRONG material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(5); // TEXTURED_GOLD_STRONG
        }
      }
    }
    glutPostRedisplay( );
  } // end if
  else if( key == '6' )
  {
    // Set TEXTURED_NEUTRAL material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(6); // TEXTURED_NEUTRAL
        }
      }
    }
    glutPostRedisplay( );
  } // end if
  else if( key == '7' )
  {
    // Set RUBBER_RED material
    for( PUJ_GL::Object* obj: this->m_Scene.get_objects() )
    {
      if( auto* meshObj = dynamic_cast<PUJ_GL::MeshObject*>(obj) )
      {
        if( PUJ_GL::Mesh* mesh = meshObj->get_mesh() )
        {
          mesh->set_material(7); // RUBBER_RED
        }
      }
    }
    glutPostRedisplay( );
  } // end if
}

// eof - App.cxx
