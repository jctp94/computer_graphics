#include <iostream>

int main( int argc, char** argv )
{
  int w = std::atoi( argv[ 1 ] );
  int h = std::atoi( argv[ 2 ] );
  int m = std::atoi( argv[ 3 ] );
  int c1_1  = std::atoi( argv[ 4 ] );
  int c1_2  = std::atoi( argv[ 5 ] );
  int c1_3  = std::atoi( argv[ 6 ] );
  int c2_1  = std::atoi( argv[ 7 ] );
  int c2_2  = std::atoi( argv[ 8 ] );
  int c2_3  = std::atoi( argv[ 9 ] );
  char* out_file = argv[ 10 ];

  int s = w * h * 3;
  char* framebuffer = std::calloc( s, 1 );
  std::memset( framebuffer, s, 0 );

  framebuffer[ 0 ] = c1_1;
  framebuffer[ 1 ] = c1_2;
  framebuffer[ 2 ] = c1_3;

  framebuffer[ s - 3 ] = c2_1;
  framebuffer[ s - 2 ] = c2_2;
  framebuffer[ s - 1 ] = c2_3;

  // Ciclo de llenado

  // Guardar en un archivo ppm
  std::cout << "P3" << std::endl;
  std::cout << "# Mi bonito resultado de interpolar colores" << std::endl;
  std::cout << w << " " << h << std::endl;
  std::cout << "255" << std::endl;
  for( int i = 0; i < s; ++i )
    std::cout << framebuffer[ i ] << std::endl;

  std::free( framebuffer );
  return( EXIT_SUCCESS );
}

// eof


