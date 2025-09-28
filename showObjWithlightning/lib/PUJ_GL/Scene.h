// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Scene__h__
#define __PUJ_GL__Scene__h__

#include <PUJ_GL/Object.h>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT Scene
  {
    PUJ_GL_Traits;

  public:
    using Self = Scene;

  public:
    Scene( );
    virtual ~Scene( );

    virtual void draw( );

    const TReal* clear_color( ) const;
    const TReal* bounding_box( ) const;

    void load_mesh( const std::string& fname );
    void load_orthobase( const TReal& s = 1 );

  protected:
    void _reset( );

  protected:
    TReal m_Color[ 4 ] { 0, 0, 0, 1 };

    mutable bool m_BoudingBoxUpdated { false };
    mutable TReal m_BoundingBox[ 6 ] { 0 };

    std::vector< PUJ_GL::Object* > m_Objects;
  };
} // end namespace

#endif // __PUJ_GL__Scene__h__

// eof - Scene.h
