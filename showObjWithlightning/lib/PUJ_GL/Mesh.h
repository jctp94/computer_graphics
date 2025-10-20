// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Mesh__h__
#define __PUJ_GL__Mesh__h__

#include <PUJ_GL/Traits.h>
#include <string>
#include <vector>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT Mesh
  {
  public:
    using Self     = Mesh;
    using TNatural = unsigned short;
    using TReal    = float;

  public:
    Mesh( );
    virtual ~Mesh( );

    const TReal* bounding_box( ) const;
    bool read_from_OBJ( const std::string& fname );
    void draw( );

  protected:
    TReal m_Color[ 3 ];
    TReal m_BoundingBox[ 6 ];

    std::vector< TReal > m_Points;
    std::vector< TReal > m_Normals;

    std::vector< TNatural > m_Edges;
    std::vector< TNatural > m_Triangles;
    std::vector< TNatural > m_Quads;

    std::vector< TNatural > m_EdgesNormals;
    std::vector< TNatural > m_TrianglesNormals;
    std::vector< TNatural > m_QuadsNormals;
  };
} // end namespace

#endif // __PUJ_GL__Mesh__h__

// eof - Mesh.h
