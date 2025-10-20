// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Mesh.h>
#include <fstream>
#include <sstream>
#include <GL/gl.h>

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
Mesh( )
{
  this->m_Color[ 0 ] = 1;
  this->m_Color[ 1 ] = 1;
  this->m_Color[ 2 ] = 1;
}

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
~Mesh( )
{
}

// -------------------------------------------------------------------------
const PUJ_GL::Mesh::
TReal* PUJ_GL::Mesh::
bounding_box( ) const
{
  return( this->m_BoundingBox );
}

// -------------------------------------------------------------------------
bool PUJ_GL::Mesh::
read_from_OBJ( const std::string& fname )
{
  this->m_Points.clear( );
  this->m_Normals.clear( );
  this->m_Edges.clear( );
  this->m_Triangles.clear( );
  this->m_Quads.clear( );
  this->m_EdgesNormals.clear( );
  this->m_TrianglesNormals.clear( );
  this->m_QuadsNormals.clear( );

  // Read file into a memory buffer
  std::ifstream obj_file( fname.c_str( ), std::ios::binary | std::ios::ate );
  if( !obj_file.is_open( ) )
    return( false );
  std::streamsize file_size = obj_file.tellg();
  obj_file.seekg( 0, std::ios::beg );
  std::vector< char > obj_buffer( file_size );
  bool ok = bool( obj_file.read( obj_buffer.data( ), file_size ) );
  obj_file.close( );
  if( !ok )
    return( false );

  // Create stream
  std::istringstream obj_str( obj_buffer.data( ) );

  // Read line-by-line
  std::string line;
  while( std::getline( obj_str, line ) )
  {
    std::istringstream line_str( line );
    std::string cmd;
    line_str >> cmd;

    if( cmd == "v" )
    {
      TReal x, y, z;
      line_str >> x >> y >> z;
      if( this->m_Points.size( ) > 0 )
      {
        this->m_BoundingBox[ 0 ] = std::min( x, this->m_BoundingBox[ 0 ] );
        this->m_BoundingBox[ 2 ] = std::min( y, this->m_BoundingBox[ 2 ] );
        this->m_BoundingBox[ 4 ] = std::min( z, this->m_BoundingBox[ 4 ] );

        this->m_BoundingBox[ 1 ] = std::max( x, this->m_BoundingBox[ 1 ] );
        this->m_BoundingBox[ 3 ] = std::max( y, this->m_BoundingBox[ 3 ] );
        this->m_BoundingBox[ 5 ] = std::max( z, this->m_BoundingBox[ 5 ] );
      }
      else
      {
        this->m_BoundingBox[ 0 ] = this->m_BoundingBox[ 1 ] = x;
        this->m_BoundingBox[ 2 ] = this->m_BoundingBox[ 3 ] = y;
        this->m_BoundingBox[ 4 ] = this->m_BoundingBox[ 5 ] = z;
      } // end if
      this->m_Points.push_back( x );
      this->m_Points.push_back( y );
      this->m_Points.push_back( z );
    }
    if( cmd == "vn" )
    {
      TReal x, y, z, n;
      line_str >> x >> y >> z;

      n = std::sqrt( ( x * x ) + ( y * y ) + ( z * z ) );
      if( n == TReal( 0 ) ) n = TReal( 1 );

      this->m_Normals.push_back( x / n );
      this->m_Normals.push_back( y / n );
      this->m_Normals.push_back( z / n );
    }
    else if( cmd == "f" )
    {
      std::vector< TNatural > idx;
      std::string tok;
      TNatural ntoks = 0;
      while( line_str >> tok )
      {
        for( auto& v: tok )
          if( v == '/' )
            v = ' ';

        std::istringstream tok_str( tok );
        TNatural i;
        while( tok_str >> i )
          idx.push_back( i - 1 );

        ntoks++;
      } // end while

      if( ntoks == idx.size( ) )
      {
        std::vector< TNatural >* o = nullptr;
        if     ( ntoks == 2 ) o = &( this->m_Edges );
        else if( ntoks == 3 ) o = &( this->m_Triangles );
        else if( ntoks == 4 ) o = &( this->m_Quads );
        if( o != nullptr )
          o->insert( o->end( ), idx.begin( ), idx.end( ) );
      }
      else if( idx.size( ) / ntoks == 2 )
      {
        if( ntoks == 2 )
        {
          for( size_t i = 0; i < idx.size( ); i += 2 )
          {
            this->m_Edges.push_back( idx[ i ] );
            this->m_EdgesNormals.push_back( idx[ i + 1 ] );
          } // end for
        }
        else if( ntoks == 3 )
        {
          for( size_t i = 0; i < idx.size( ); i += 2 )
          {
            this->m_Triangles.push_back( idx[ i ] );
            this->m_TrianglesNormals.push_back( idx[ i + 1 ] );
          } // end for
        }
        else if( ntoks == 4 )
        {
          for( size_t i = 0; i < idx.size( ); i += 2 )
          {
            this->m_Quads.push_back( idx[ i ] );
            this->m_QuadsNormals.push_back( idx[ i + 1 ] );
          } // end for
        } // end if
      }
      else if( idx.size( ) / ntoks == 3 )
      {
        if( ntoks == 2 )
        {
          for( size_t i = 0; i < idx.size( ); i += 3 )
          {
            this->m_Edges.push_back( idx[ i ] );
            this->m_EdgesNormals.push_back( idx[ i + 2 ] );
          } // end for
        }
        else if( ntoks == 3 )
        {
          for( size_t i = 0; i < idx.size( ); i += 3 )
          {
            this->m_Triangles.push_back( idx[ i ] );
            this->m_TrianglesNormals.push_back( idx[ i + 2 ] );
          } // end for
        }
        else if( ntoks == 4 )
        {
          for( size_t i = 0; i < idx.size( ); i += 3 )
          {
            this->m_Quads.push_back( idx[ i ] );
            this->m_QuadsNormals.push_back( idx[ i + 2 ] );
          } // end for
        } // end if
      } // end if
    } // end if

  } // end while

  // Free unneeded memory
  this->m_Points.shrink_to_fit( );
  this->m_Normals.shrink_to_fit( );
  this->m_Edges.shrink_to_fit( );
  this->m_Triangles.shrink_to_fit( );
  this->m_Quads.shrink_to_fit( );
  this->m_EdgesNormals.shrink_to_fit( );
  this->m_TrianglesNormals.shrink_to_fit( );
  this->m_QuadsNormals.shrink_to_fit( );

  return( true );
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
draw( )
{
  glColor3fv( this->m_Color );

  const TReal* p = this->m_Points.data( );
  const TReal* n = this->m_Normals.data( );

  glBegin( GL_LINES );
  {
    for( size_t i = 0; i < this->m_Edges.size( ); ++i )
    {
      if( this->m_EdgesNormals.size( ) > 0 )
        glNormal3fv( n + ( this->m_EdgesNormals[ i ] * 3 ) );
      glVertex3fv( p + ( this->m_Edges[ i ] * 3 ) );
    } // end for
  }
  glEnd( );

  bool has_triangles_normals = ( this->m_TrianglesNormals.size( ) > 0 );
  for( size_t i = 0; i < this->m_Triangles.size( ); i += 3 )
  {
    glBegin( GL_LINE_LOOP );
    {
      if( has_triangles_normals )
        glNormal3fv( n + ( this->m_TrianglesNormals[ i ] * 3 ) );
      glVertex3fv( p + ( this->m_Triangles[ i ] * 3 ) );

      if( has_triangles_normals )
        glNormal3fv( n + ( this->m_TrianglesNormals[ i + 1 ] * 3 ) );
      glVertex3fv( p + ( this->m_Triangles[ i + 1 ] * 3 ) );

      if( has_triangles_normals )
        glNormal3fv( n + ( this->m_TrianglesNormals[ i + 2 ] * 3 ) );
      glVertex3fv( p + ( this->m_Triangles[ i + 2 ] * 3 ) );
    }
    glEnd( );
  } // end for

  bool has_quads_normals = ( this->m_TrianglesNormals.size( ) > 0 );
  for( size_t i = 0; i < this->m_Quads.size( ); i += 4 )
  {
    glBegin( GL_LINE_LOOP );
    {
      if( has_quads_normals )
        glNormal3fv( n + ( this->m_QuadsNormals[ i ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i ] * 3 ) );

      if( has_quads_normals )
        glNormal3fv( n + ( this->m_QuadsNormals[ i + 1 ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 1 ] * 3 ) );

      if( has_quads_normals )
        glNormal3fv( n + ( this->m_QuadsNormals[ i + 2 ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 2 ] * 3 ) );

      if( has_quads_normals )
        glNormal3fv( n + ( this->m_QuadsNormals[ i + 3 ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 3 ] * 3 ) );
    }
    glEnd( );
  } // end for
}

// eof - Mesh.cxx
