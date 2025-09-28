// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/ParametricModel.h>
#include <vector>
#include <cmath> // For std::sqrt
#include <iostream> // Para depuración

// -------------------------------------------------------------------------
PUJ_GL::ParametricModel::
ParametricModel( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::ParametricModel::
~ParametricModel( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_parameters_ranges(
  const TReal& minU, const TReal& maxU, const TReal& minV, const TReal& maxV
  )
{
  this->m_MinU = minU;
  this->m_MaxU = maxU;
  this->m_MinV = minV;
  this->m_MaxV = maxV;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_parameters_closeness( const bool& u, const bool& v )
{
  this->m_ClosedU = u;
  this->m_ClosedV = v;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_number_of_samples( const TNatural& u, const TNatural& v )
{
  this->m_SamplesU = u;
  this->m_SamplesV = v;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
build( TParametricFunction f )
{
  TReal ou = this->m_MaxU - this->m_MinU;
  TReal ov = this->m_MaxV - this->m_MinV;
  TNatural SU = this->m_SamplesU - ( ( this->m_ClosedU )? 0: 1 );
  TNatural SV = this->m_SamplesV - ( ( this->m_ClosedV )? 0: 1 );

  // Compute sizes
  this->m_NumberOfVertices =
    this->m_NumberOfNormals =
    this->m_NumberOfTextures = this->m_SamplesU * this->m_SamplesV;

  std::cout << "Generando modelo con " << this->m_NumberOfVertices << " vértices." << std::endl;

  // Reserve buffers
  this->m_Vertices = reinterpret_cast< TReal* >( std::calloc( this->m_NumberOfVertices * 3, sizeof( TReal ) ) );
  this->m_Normals = reinterpret_cast< TReal* >( std::calloc( this->m_NumberOfNormals * 3, sizeof( TReal ) ) );
  this->m_Textures = reinterpret_cast< TReal* >( std::calloc( this->m_NumberOfTextures * 2, sizeof( TReal ) ) );

  TReal* points = this->m_Vertices;
  TReal* normals = this->m_Normals;
  TReal* textures = this->m_Textures;
  size_t n_faces = 2 * ( this->m_SamplesU - 1 ) * ( this->m_SamplesV - 1 );
  TNatural* indices = reinterpret_cast< TNatural* >( std::calloc( n_faces * 9, sizeof( TNatural ) ) );
  TNatural* idx = indices;

  // Inicializar bounding box con valores extremos
  TReal min_x = std::numeric_limits<TReal>::max(), min_y = min_x, min_z = min_x;
  TReal max_x = -min_x, max_y = max_x, max_z = max_x;

  // Temporary buffers for partial derivatives
  TReal du_vec[3];
  TReal dv_vec[3];

  for( TNatural su = 0; su < this->m_SamplesU; ++su )
  {
    TReal nu = ( TReal( su ) / TReal( SU ) );
    TReal u = ( ou * nu ) + this->m_MinU;
    for( TNatural sv = 0; sv < this->m_SamplesV; ++sv )
    {
      TReal nv = ( TReal( sv ) / TReal( SV ) );
      TReal v = ( ov * nv ) + this->m_MinV;

      // Llamar a la función paramétrica para obtener el punto y las derivadas parciales
      f( points, normals, du_vec, dv_vec, u, v );

      // Calcular la normal como el producto cruz de las derivadas parciales
      normals[0] = du_vec[1] * dv_vec[2] - du_vec[2] * dv_vec[1];
      normals[1] = du_vec[2] * du_vec[0] - du_vec[0] * dv_vec[2];
      normals[2] = du_vec[0] * dv_vec[1] - du_vec[1] * du_vec[0];

      // Normalizar el vector normal
      TReal normal_length = std::sqrt(normals[0]*normals[0] + normals[1]*normals[1] + normals[2]*normals[2]);
      if (normal_length > 1e-6) {
          normals[0] /= normal_length;
          normals[1] /= normal_length;
          normals[2] /= normal_length;
      }

      // Actualizar bounding box con el punto actual
      if (points[0] < min_x) min_x = points[0];
      if (points[1] < min_y) min_y = points[1];
      if (points[2] < min_z) min_z = points[2];
      if (points[0] > max_x) max_x = points[0];
      if (points[1] > max_y) max_y = points[1];
      if (points[2] > max_z) max_z = points[2];

      // Create triangles (sin cambios)
      if( su < this->m_SamplesU - 1 && sv < this->m_SamplesV - 1 )
      {
        size_t w = su + ( this->m_SamplesU * sv ) + 1;

        // Triangle 1
        *( idx++ ) = w; *( idx++ ) = w; *( idx++ ) = w;
        *( idx++ ) = w + 1; *( idx++ ) = w + 1; *( idx++ ) = w + 1;
        *( idx++ ) = w + 1 + this->m_SamplesU; *( idx++ ) = w + 1 + this->m_SamplesU; *( idx++ ) = w + 1 + this->m_SamplesU;

        // Triangle 2
        *( idx++ ) = w; *( idx++ ) = w; *( idx++ ) = w;
        *( idx++ ) = w + 1 + this->m_SamplesU; *( idx++ ) = w + 1 + this->m_SamplesU; *( idx++ ) = w + 1 + this->m_SamplesU;
        *( idx++ ) = w + this->m_SamplesU; *( idx++ ) = w + this->m_SamplesU; *( idx++ ) = w + this->m_SamplesU;
      }

      // Texture coordinates
      textures[ 0 ] = nu;
      textures[ 1 ] = nv;

      points += 3;
      normals += 3;
      textures += 2;
    }
  }

  // Asignar bounding box calculado
  this->m_BoundingBox[0] = min_x; this->m_BoundingBox[1] = min_y; this->m_BoundingBox[2] = min_z;
  this->m_BoundingBox[3] = max_x; this->m_BoundingBox[4] = max_y; this->m_BoundingBox[5] = max_z;

  std::cout << "Bounding Box del modelo: min(" << min_x << "," << min_y << "," << min_z 
            << ") max(" << max_x << "," << max_y << "," << max_z << ")" << std::endl;

  // Create topology (sin cambios)
  TFaces triangles( n_faces, indices );
  TPolygons polys;
  TGroups group;

  polys.insert( std::make_pair( 3, triangles ) );
  group.insert( std::make_pair( "parametric_group", polys ) );
  this->m_Objects.insert( std::make_pair( "parametric_object", group ) );

  // Llamar al método padre para cualquier actualización adicional
  this->_update_bounding_box( );  // Si existe en Mesh, llamarlo para consistencia
}
// -------------------------------------------------------------------------
// eof - ParametricModel.cxx
