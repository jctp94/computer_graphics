// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================
#ifndef __ShowOBJApp__h__
#define __ShowOBJApp__h__

#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/TrackballCamera.h>

/**
 */
class ShowOBJApp
  : public PUJ_GL::BaseApp
{
  PUJ_GL_Traits;

public:
  using Self       = ShowOBJApp;
  using Superclass = PUJ_GL::BaseApp;

public:
  ShowOBJApp(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10, int y = 10
    );
  virtual ~ShowOBJApp( ) override;

  virtual void init( ) override;

protected:
  virtual void _cb_reshape( int width, int height ) override;
  virtual void _cb_display( ) override;
  virtual void _cb_mouse( int button, int state, int x, int y ) override;
  virtual void _cb_special( int key, int x, int y ) override;
  virtual void _cb_keyboard( unsigned char key, int x, int y ) override;

protected:
  PUJ_GL::TrackballCamera m_Camera;
};

#endif // __ShowOBJApp__h__

// eof - ShowOBJApp.h
