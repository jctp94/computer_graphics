// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <stdio.h>
#include <GL/glut.h>

// -------------------------------------------------------------------------
int WindowID;

// -------------------------------------------------------------------------
void create_window( int* argc, char* argv[] );
void init_window( );
void register_callbacks( );
void go( );

// -------------------------------------------------------------------------
void cb_display( );
void cb_keyboard( unsigned char key, int x, int y );
void cb_special_keyboard( int key, int x, int y );

// -------------------------------------------------------------------------
int main( int argc, char* argv[] )
{
  create_window( &argc, argv );
  init_window( );
  register_callbacks( );
  go( );

  return( 0 );
}

// -------------------------------------------------------------------------
void create_window( int* argc, char* argv[] )
{
  glutInit( argc, argv );
  glutInitDisplayMode( GLUT_SINGLE | GLUT_RGB );
  glutInitWindowSize( 500, 500 );
  glutInitWindowPosition( 100, 100 );
  WindowID = glutCreateWindow( "Hello World!" );
}

// -------------------------------------------------------------------------
void init_window( )
{
  glClearColor( 0.0, 0.0, 0.0, 1.0 );
}

// -------------------------------------------------------------------------
void register_callbacks( )
{
  glutDisplayFunc( cb_display );
  glutKeyboardFunc( cb_keyboard );
  glutSpecialFunc( cb_special_keyboard );

  // glutReshapeFunc
  // glutOverlayDisplayFunc
  // glutMouseFunc
  // glutMotionFunc
  // glutPassiveMotionFunc
  // glutVisibilityFunc
  // glutEntryFunc
  // glutSpaceballMotionFunc
  // glutSpaceballRotateFunc
  // glutSpaceballButtonFunc
  // glutButtonBoxFunc
  // glutDialsFunc
  // glutTabletMotionFunc
  // glutTabletButtonFunc
  // glutMenuStatusFunc
  // glutIdleFunc
  // glutTimerFunc
}

// -------------------------------------------------------------------------
void go( )
{
  glutMainLoop( );
}

// -------------------------------------------------------------------------
void cb_display( )
{
  float BB[ 4 ] = { 53, 20, 200, 100 };
  float cog[ 2 ], scl[ 2 ];
  cog[ 0 ] = ( BB[ 2 ] + BB[ 0 ] ) * 0.5;  
  cog[ 1 ] = ( BB[ 3 ] + BB[ 1 ] ) * 0.5;  
  scl[ 0 ] = 2.0 / ( BB[ 2 ] - BB[ 0 ] );  
  scl[ 1 ] = 2.0 / ( BB[ 3 ] - BB[ 1 ] );  

  glClear( GL_COLOR_BUFFER_BIT );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  glScalef( scl[ 0 ], scl[ 1 ], 1 );
  glTranslatef( -cog[ 0 ], -cog[ 1 ], 0 );

  glBegin( GL_POLYGON );
  /*
     GL_POINTS
     GL_LINES
     GL_LINE_STRIP
     GL_LINE_LOOP
     GL_TRIANGLES
     GL_TRIANGLE_STRIP
     GL_TRIANGLE_FAN
     GL_QUADS
     GL_QUAD_STRIP
     GL_POLYGON
  */
  {
    glColor3f( 1, 1, 1 );
    glVertex2f( 100.0, 50.0 );

    glColor3f( 1, 0, 0 );
    glVertex2f( 53, 20 );

    glColor3f( 0, 1, 0 );
    glVertex2f( 200.0, 100 );
  }
  glEnd( );

  glFlush( );
}

// -------------------------------------------------------------------------
void cb_keyboard( unsigned char key, int x, int y )
{
  printf( "Keyboard: %d %d %d\n", key, x, y );
}

// -------------------------------------------------------------------------
void cb_special_keyboard( int key, int x, int y )
{
  printf( "Special: %d %d %d\n", key, x, y );
}

// eof - main.c
