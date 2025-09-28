// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__MeshObject__h__
#define __PUJ_GL__MeshObject__h__

#include <PUJ_GL/Object.h>
#include <PUJ_GL/Mesh.h> // Incluir Mesh para la declaración de m_Mesh

namespace PUJ_GL
{
  // Forward declaration
  // class Mesh; // Ya no es forward declaration si se incluye el .h

  /**
   */
  class PUJ_GL_EXPORT MeshObject
    : public PUJ_GL::Object
  {
    PUJ_GL_Traits;

  public:
    using Self       = MeshObject;
    using Superclass = PUJ_GL::Object;

  public:
    MeshObject( );
    virtual ~MeshObject( ) override;

    virtual void set_mesh( PUJ_GL::Mesh* mesh );
    virtual void read( const std::string& fname );

    virtual void draw( ) override;

  public: // Cambiado a public para acceso desde App.cxx
    PUJ_GL::Mesh* m_Mesh { nullptr };
  };
} // end namespace

#endif // __PUJ_GL__MeshObject__h__

// eof - MeshObject.h