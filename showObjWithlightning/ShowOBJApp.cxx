// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include "ShowOBJApp.h"

// -------------------------------------------------------------------------
ShowOBJApp::
ShowOBJApp(
  int* argc, char** argv,
  int w, int h,
  int x, int y
  )
  : Superclass(
    argc, argv, GLUT_DOUBLE | GLUT_RGB, w, h, x, y, "Show OBJ models"
    )
{
  this->m_Scene.load_mesh( argv[ 1 ] );
  this->m_Camera.configure( this->m_Scene.bounding_box( ) );
  this->m_Scene.load_orthobase( 0.1 );
}

// -------------------------------------------------------------------------
ShowOBJApp::
~ShowOBJApp( )
{
}

// -------------------------------------------------------------------------
void ShowOBJApp::
init( )
{
  this->Superclass::init( );
  const TReal* c = this->m_Scene.clear_color( );
  glClearColor( c[ 0 ], c[ 1 ], c[ 2 ], c[ 3 ] );
}

// -------------------------------------------------------------------------
void ShowOBJApp::
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
void ShowOBJApp::
_cb_display( )
{
  glClear( GL_COLOR_BUFFER_BIT );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  this->m_Camera.look( );
  this->m_Scene.draw( );
  glutSwapBuffers( );
}

// -------------------------------------------------------------------------
void ShowOBJApp::
_cb_mouse( int button, int state, int x, int y )
{
  if( state == 1 && ( button == 3 || button == 4 ) )
  {
    this->m_Camera.zoom( 1e-1 * TReal( ( button == 3 )? -1: 1 ) );
    glutPostRedisplay( );
  } // end if
}

// -------------------------------------------------------------------------
void ShowOBJApp::
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
void ShowOBJApp::
_cb_keyboard( unsigned char key, int x, int y )
{
  if( key == 'r' || key == 'R' )
  {
    this->m_Camera.reset( );
    glutPostRedisplay( );
  } // end if
}

// eof - ShowOBJApp.cxx
