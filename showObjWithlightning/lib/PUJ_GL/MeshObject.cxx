// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/MeshObject.h>
#include <PUJ_GL/Mesh.h>

// -------------------------------------------------------------------------
PUJ_GL::MeshObject::
MeshObject( const std::string& fname )
{
  this->m_Mesh = new PUJ_GL::Mesh( );
  this->m_Mesh->read_from_OBJ( fname );
  std::memcpy(
    this->m_BoundingBox, this->m_Mesh->bounding_box( ), 6 * sizeof( TReal )
    );
}

// -------------------------------------------------------------------------
PUJ_GL::MeshObject::
~MeshObject( )
{
  if( this->m_Mesh != nullptr )
    delete this->m_Mesh;
}

// -------------------------------------------------------------------------
void PUJ_GL::MeshObject::
draw( )
{
  if( this->m_Mesh != nullptr )
    this->m_Mesh->draw( );
}

// eof - MeshObject.cxx
