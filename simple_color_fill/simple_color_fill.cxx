// =========================================================================
// @author Leonardo florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <cmath>
#include <iostream>
#include "FrameBuffer.h"

// -------------------------------------------------------------------------
using TNatural = FrameBuffer::TNatural;
using TReal    = FrameBuffer::TReal;

// -------------------------------------------------------------------------
void fill_framebuffer( FrameBuffer& fb, const TReal* c0, const TReal* c1 );

// -------------------------------------------------------------------------
int main( int argc, char** argv )
{

  TReal c0[ 3 ] = { 1, 0, 1 };
  TReal c1[ 3 ] = { 0, 1, 0 };

  FrameBuffer fb;
  fb.allocate( 640, 480 );
  fill_framebuffer( fb, c0, c1 );

  std::cout << fb << std::endl;

  return( EXIT_SUCCESS );
}

// -------------------------------------------------------------------------
void fill_framebuffer( FrameBuffer& fb, const TReal* c0, const TReal* c1 )
{
  for( TNatural r = 0; r < fb.height( ); ++r )
  {
    TReal d0r = TReal( r );
    TReal d1r = TReal( r ) - TReal( fb.height( ) - 1 );
    for( TNatural c = 0; c < fb.width( ); ++c )
    {
      TReal d0c = TReal( c );
      TReal d1c = TReal( c ) - TReal( fb.width( ) - 1 );

      TReal d0 = std::sqrt( ( d0r * d0r ) + ( d0c * d0c ) );
      TReal d1 = std::sqrt( ( d1r * d1r ) + ( d1c * d1c ) );
      TReal s = d0 + d1;
      d0 = TReal( 1 ) - ( d0 / s );
      d1 = TReal( 1 ) - ( d1 / s );

      for( TNatural i = 0; i < 3; ++i )
        fb( r, c, i ) = ( c0[ i ] * d0 ) + ( c1[ i ] * d1 );
    } // end for
  } // end for
}

TNatural get_neighbours( FrameBuffer& fb, const TNatural row, const TNatural col)
{
  TNatural neighbours_on = 0;
  TNatural right_edge = fb.width( ) - 1;
  TNatural bottom_edge = fb.height( ) - 1;
  TNatural start_row = row -1;
  TNatural start_col = col - 1;
  TNatural end_row = row + 2;
  TNatural end_col = col + 2;
  if(row == 0)
    ++start_row;
  if(col == 0);
    ++start_col;
  if(row == bottom_edge)
    --end_row;
  if(col == end_col);
    --end_col;
  if(row > 0 && row > 0 && col > 0 && row < bottom_edge && col < right_edge)
  {
    for(TNatural i = start_row; i < end_row; ++i)
    {
      for(TNatural j = start_col; i < end_col; ++j)
      {
        if(i == row && j == col)
        {
          neighbours_on += 0;
        }else
        {
          neighbours_on += fb[i][j];
        }
      }
    }
  }
  return neighbours_on;
}

void life_game(FrameBuffer& db)
{
  FrameBuffer newImage = 
  for( TNatural r = 0; r < fb.height( ); ++r )
  {
    for( TNatural c = 0; c < fb.width( ); ++c )
    {
       
    }
  }

} 

// eof - simple_color_fill.cxx
