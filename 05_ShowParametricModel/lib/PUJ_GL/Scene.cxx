// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Scene.h>
#include <PUJ_GL/MeshObject.h>
#include <PUJ_GL/OrthoBase.h>
#include <PUJ_GL/ParametricModel.h>
#include <PUJ_GL/Image.h>  // Para Image*
#include <algorithm>       // Para std::min y std::max
#include <cstring>         // Para std::memcpy
#include <cmath>           // Para cálculos

// -------------------------------------------------------------------------
PUJ_GL::Scene::
Scene( )
{
  // Inicialización por defecto
}

// -------------------------------------------------------------------------
PUJ_GL::Scene::
~Scene( )
{
  this->_reset( );
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
draw( )
{
  for( PUJ_GL::Object* o: this->m_Objects )
    if( o != nullptr )  // Chequeo de seguridad
      o->draw( );
}

// -------------------------------------------------------------------------
const PUJ_GL::Scene::
TReal* PUJ_GL::Scene::
clear_color( ) const
{
  return( this->m_Color );
}

// -------------------------------------------------------------------------
const PUJ_GL::Scene::
TReal* PUJ_GL::Scene::
bounding_box( ) const
{
  if( !( this->m_BoundingBoxUpdated ) )
  {
    if( this->m_Objects.size( ) > 0 )
    {
      // memcpy: Ahora m_BoundingBox es mutable, así que es TReal* (no const)
      std::memcpy(
        this->m_BoundingBox,  // Directo: mutable permite escritura
        this->m_Objects[ 0 ]->bounding_box( ),
        6 * sizeof( TReal )
        );
      for( size_t i = 1; i < this->m_Objects.size( ); ++i )
      {
        for( unsigned short d = 0; d < 3; ++d )
        {
          // Asignaciones directas: mutable permite modificación
          this->m_BoundingBox[ d << 1 ]
            =
            std::min(
              this->m_BoundingBox[ d << 1 ],
              this->m_Objects[ i ]->bounding_box( )[ d << 1 ]
              );
          this->m_BoundingBox[ ( d << 1 ) + 1 ]
            =
            std::max(
              this->m_BoundingBox[ ( d << 1 ) + 1 ],
              this->m_Objects[ i ]->bounding_box( )[ ( d << 1 ) + 1 ]
              );
        } // end for
      } // end for
    } // end if
    // Bandera: mutable, no necesita const_cast
    this->m_BoundingBoxUpdated = true;
  } // end if
  return( this->m_BoundingBox );
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_mesh( const std::string& fname )
{
  auto obj = new PUJ_GL::MeshObject( );
  obj->read( fname );
  this->m_Objects.push_back( obj );
  this->m_BoundingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_orthobase( const TReal& s )
{
  this->m_Objects.push_back( new PUJ_GL::OrthoBase( s ) );
  this->m_BoundingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_parametric_model(
  TParametricFunction function,  // Firma nueva (con du, dv)
  const TReal& minU, const TReal& maxU,
  const TNatural& samplesU, bool closedU,
  const TReal& minV, const TReal& maxV,
  const TNatural& samplesV, bool closedV,
  PUJ_GL::Image* image
  )
{
  auto obj = new PUJ_GL::MeshObject( );
  auto mesh = new PUJ_GL::ParametricModel( );
  mesh->set_parameters_ranges( minU, maxU, minV, maxV );
  mesh->set_parameters_closeness( closedU, closedV );
  mesh->set_number_of_samples( samplesU, samplesV );
  mesh->build( function );  // Firma correcta
  if( image != nullptr )
    mesh->set_image( image );
  obj->set_mesh( mesh );
  this->m_Objects.push_back( obj );
  this->m_BoundingBoxUpdated = false;
}

// -------------------------------------------------------------------------
PUJ_GL::MeshObject* PUJ_GL::Scene::
get_last_object( ) const
{
  if( !m_Objects.empty() && m_Objects.back() != nullptr )
  {
    return dynamic_cast<PUJ_GL::MeshObject*>( m_Objects.back() );
  }
  return nullptr;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
reset( )
{
  this->_reset( );
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
_reset( )
{
  for( PUJ_GL::Object* o: this->m_Objects )
    if( o != nullptr )
      delete o;
  this->m_Objects.clear( );
  this->m_BoundingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
_update_bounding_box( )
{
  // Forzar actualización del cache: llama al método const y ignora retorno
  (void)this->bounding_box();  // Cast a void para suprimir warning de unused return
}

// eof - Scene.cxx
