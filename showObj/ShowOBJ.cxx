// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include <iostream>
#include <Eigen/Core>
#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/Mesh.h>

/**
 */
class MyApp
  : public PUJ_GL::BaseApp
{
public:
  using Self       = MyApp;
  using Superclass = PUJ_GL::BaseApp;

  using TReal = PUJ_GL::Mesh::TReal;
  using TMatrix = Eigen::Matrix< TReal, 4, 4 >;
  static TMatrix Tfrom(const Eigen::Matrix<TReal,3,1>& t) {
    TMatrix T = TMatrix::Identity();
    // 1 0 0 t(0)
    // 0 1 0 t(1)
    // 0 0 1 t(2)
    // 0 0 0 1
    T(0,3) = t(0); T(1,3) = t(1); T(2,3) = t(2);
    return T;
  }
  static TMatrix Sfrom(TReal s) {
    TMatrix S = TMatrix::Identity();
    S(0,0) = S(1,1) = S(2,2) = s;
    return S;
  }
  float g_fovy_deg = 45.0f;    // FOV vertical en grados
  float g_near     = 0.1f;     // plano cercano (positivo)
  float g_far      = 1000.0f;
  
  Eigen::Matrix<TReal,3,1> m_Pivot { 0, 0, 0 };

public:
  MyApp(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10, int y = 10
    )
    : Superclass(
      argc, argv,
      GLUT_DOUBLE | GLUT_RGB,
      w, h, x, y, "Show OBJ models"
      )
    { 
      this->m_Camera.setIdentity( );

      this->m_Mesh.read_from_OBJ( argv[ 1 ] );
      const float* bb = m_Mesh.bounding_box(); // {minX, maxX, minY, maxY, minZ, maxZ}
      // Code to calculate the center of the object and assign it to the pivot
      // Eigen::Vector3f pivot( (bb[0]+bb[1])*0.5f,
      //                        (bb[2]+bb[3])*0.5f,
      //                        (bb[4]+bb[5])*0.5f );

      // rotar sobre el centro del objeto                             
      // m_Pivot = pivot;
      this->view = argv[ 2 ] ? argv[ 2 ] : "ortho";
    }

  virtual ~MyApp( ) override
    {
    }

  virtual void init( ) override
    {
      this->Superclass::init( );
      
      glClearColor( 0.0, 0.0, 0.0, 1.0 );
      glEnable(GL_DEPTH_TEST);

    }

protected:
  virtual void _cb_reshape( int width, int height ) override
    {
      TReal a = 1.0;

      if( height != 0 )
        a = TReal( width ) / TReal( height );

      glViewport( 0, 0, width, height );

      glMatrixMode( GL_PROJECTION );
      glLoadIdentity( );
      
      float aspect = (height > 0) ? float(width)/float(height) : 1.0f;
      float fovy   = g_fovy_deg * float(M_PI) / 180.0f;

      // Deriva “top” y “right” en el plano near a partir del FOV
      float top   = g_near * std::tan(0.5f * fovy);
      float right = top * aspect;

      if (this->view == "ortho") {
        // glOrtho( left, right, bottom, up, near, far );
        glOrtho(-2, 2, -2, 2, -2, 2);
      } else if (this->view == "frustum") {
        // glFrustum( left, right, bottom, up, near, far );
        glFrustum(-right, right, -top, top, g_near, g_far);
        glTranslatef(0, 0, -1);

      } else if (this->view == "perspective") {
        // gluPerspective( fovy, aspect, near, far );
        gluPerspective(g_fovy_deg, a, g_near, g_far);
        glTranslatef(0, 0, -5);
      }


      glMatrixMode(GL_MODELVIEW); 
      this->m_Camera.setIdentity();
      glutPostRedisplay( );
    }
  virtual void _cb_display( ) override
    {
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

      glMatrixMode( GL_MODELVIEW );
      glLoadIdentity( );

      // Show the global orthogonal base
      glBegin( GL_LINES );
      {
        glColor3f( 1, 0, 0 );
        glVertex3f( -0.1, 0, 0 );
        glVertex3f( 1, 0, 0 );

        glColor3f( 0, 1, 0 );
        glVertex3f( 0, -0.1, 0 );
        glVertex3f( 0, 1, 0 );

        glColor3f( 0, 0, 1 );
        glVertex3f( 0, 0, -0.1 );
        glVertex3f( 0, 0, 1 );
      }
      glEnd( );

      glPushMatrix( );
      glMultMatrixf( this->m_Camera.data( ) );


      // Show mesh
      this->m_Mesh.draw( );
      glPopMatrix( );
      glutSwapBuffers( );
    }

  virtual void _cb_keyboard( unsigned char key, int x, int y ) override
    {
      if( key == 'x' || key == 'X' )
      {
        this->m_Axis = 'x';
      }
      else if( key == 'y' || key == 'Y' )
      {
        this->m_Axis = 'y';
      }
      else if( key == 'z' || key == 'Z' )
      {
        this->m_Axis = 'z';
      }
      else if( key == 'f' || key == 'F' )
      {
        this->m_Axis = 'f';
      }
      else if( key == '+' || key == '-' )
      {
        static const TReal a = std::atan( TReal( 1 ) ) / TReal( 45 );
        static const TReal ca = std::cos( a );
        static const TReal sa = std::sin( a );

        TMatrix R = TMatrix::Identity( );

        if( this->m_Axis == 'x' )
        {
          R( 1, 1 ) = R( 2, 2 ) = ca;
          R( 1, 2 ) = R( 2, 1 ) = sa;
          if     ( key == '+' ) R( 1, 2 ) *= TReal( -1 );
          else if( key == '-' ) R( 2, 1 ) *= TReal( -1 );
        }
        else if( this->m_Axis == 'y' )
        {
          R( 0, 0 ) = R( 2, 2 ) = ca;
          R( 0, 2 ) = R( 2, 0 ) = sa;
          if     ( key == '+' ) R( 2, 0 ) *= TReal( -1 );
          else if( key == '-' ) R( 0, 2 ) *= TReal( -1 );
        }
        else if( this->m_Axis == 'z' )
        {
          R( 0, 0 ) = R( 1, 1 ) = ca;
          R( 0, 1 ) = R( 1, 0 ) = sa;
          if     ( key == '+' ) R( 0, 1 ) *= TReal( -1 );
          else if( key == '-' ) R( 1, 0 ) *= TReal( -1 );
        }
        else if (this->m_Axis == 'f') {
          // factor incremental: acercar = 1.1, alejar = 1/1.1
          TReal s = (key == '+') ? TReal(1.1) : TReal(1.0/1.1);
        
          // Zoom en ejes fijos (mundo): pre-multiplico con el sándwich T(p)*S*T(-p)
          TMatrix S = Sfrom(s);
          this->m_Camera = Tfrom(m_Pivot) * S * Tfrom(-m_Pivot) * this->m_Camera;
        
          glutPostRedisplay();
          return; // opcional: para no pasar al bloque de rotación
        }

        this->m_Camera = Tfrom(m_Pivot) * R * Tfrom(-m_Pivot) * this->m_Camera;

        glutPostRedisplay( );
      }
      else if( key == 'r' || key == 'R' )
      {
        this->m_Camera.setIdentity();
        this->m_Camera(2, 3) = 0.0;
        glutPostRedisplay( );
      } // end if
    }
  
  virtual void _cb_mouse( int button, int state, int x, int y ) override
    {
      this->lastX = x;
      this->lastY = y;
      if( button == 3 && state == GLUT_DOWN ) // scroll up
      {
        // acercar
        TReal s = TReal(1.1);
        TMatrix S = Sfrom(s);
        this->m_Camera = Tfrom(m_Pivot) * S * Tfrom(-m_Pivot) * this->m_Camera;
        glutPostRedisplay( );
      }
      else if( button == 4 && state == GLUT_DOWN ) // scroll down
      {
        // alejar
        TReal s = TReal(1.0/1.1);
        TMatrix S = Sfrom(s);
        this->m_Camera = Tfrom(m_Pivot) * S * Tfrom(-m_Pivot) * this->m_Camera;
        glutPostRedisplay( );
      }
    }

  virtual void _cb_motion( int x, int y ) override
    { 
      static const TReal a = std::atan( TReal( 1 ) ) / TReal( 10 );
      static const TReal ca = std::cos( a );
      static const TReal sa = std::sin( a );

      int sgnY = (y > lastY) ? +1 : (y < lastY ? -1 : 0);
      if (sgnY != 0) {
          TMatrix R = TMatrix::Identity();
          R(1,1) =  ca;      R(1,2) = -sgnY * sa;
          R(2,1) =  sgnY*sa; R(2,2) =  ca;
          // this->m_Camera = this->m_Camera * R;   // o R * m_Camera si usas “vista”
          this->m_Camera = Tfrom(m_Pivot) * R * Tfrom(-m_Pivot) * this->m_Camera;
      }
      // 1 0 0 0
      // 0 ca -sa 0
      // 0 sa ca 0
      // 0 0 0 1
      // this->m_Camera.transpose( ) *= R.transpose( );

      int sgnX = (x > lastX) ? +1 : (x < lastX ? -1 : 0);
      if (sgnX != 0) {
          TMatrix R = TMatrix::Identity();
          R(0,0) =  ca;      R(0,2) =  sgnX*sa;
          R(2,0) = -sgnX*sa; R(2,2) =  ca;
          // this->m_Camera = this->m_Camera * R;   // o R * m_Camera
          // this->m_Camera = this->m_Camera * Tfrom(m_Pivot) * R * Tfrom(-m_Pivot);
          this->m_Camera = Tfrom(m_Pivot) * R * Tfrom(-m_Pivot) * this->m_Camera;
      }

      //ca 0 sa 0
      // 0 1 0 0
      // -sa 0 ca 0
      // 0 0 0 1
      // this->m_Camera.transpose( ) *= R.transpose( );
      glutPostRedisplay( );
      this->lastX = x;
      this->lastY = y;
    }

protected:
  TMatrix m_Camera;
  int lastX;
  int lastY;
  unsigned char m_Axis { 'y' };
  PUJ_GL::Mesh m_Mesh;
  std::string view;
};

int main( int argc, char** argv )
{
  MyApp app( &argc, argv );
  app.init( );
  app.go( );

  return( EXIT_SUCCESS );
}

// eof - ShowOBJ.cxx
