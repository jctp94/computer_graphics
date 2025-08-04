// =========================================================================
// @author Leonardo florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <cmath>
#include <iostream>
#include "FrameBuffer.h"
#include <fstream>
#include <string>
#include <sstream>

// -------------------------------------------------------------------------
using TNatural = FrameBuffer::TNatural;
using TReal    = FrameBuffer::TReal;

int height = 0;
int weight = 0;
FrameBuffer fb;
std::set<std::pair<int, int>> postions;

// -------------------------------------------------------------------------
void fill_framebuffer( FrameBuffer& fb, const TReal* c0, const TReal* c1 );
void read_file();
void set_dims(std::string line);

// -------------------------------------------------------------------------
int main( int argc, char** argv )
{

  TReal c0[ 3 ] = { 1, 0, 1 };
  TReal c1[ 3 ] = { 0, 1, 0 };


//  fb.allocate( 10, 10 );
  //fill_framebuffer( fb, c0, c1 );

//  std::cout << fb << std::endl;
  read_file();
//  std::cout << fb << std::endl;

  return( EXIT_SUCCESS );
}

//
void read_file()
{
    std::ifstream file("board_00.pbm");  // open file for reading
    if (!file) {
        std::cerr << "Error opening file." << std::endl;
    }

    std::string line;
    int i = 0;
    while (std::getline(file, line)) {
        if(i == 2)
        {
            set_dims(line);
            fb.allocate( height, weight );
        }
        else if (i > 2){
            std::istringstream iss(line);
            int value;
            int j = 0;
            while (iss >> value) {
                if (value == 1){
                    std::cout << "1 found" << std::endl;
                }
                fb( i - 3, j, 0 ) = value;
//                std::cout << "Value in the buffer " <<  fb( i - 3, j, 0 ) << std::endl;
                j++;
            }
        }
        i++;
    }

    file.close();  // optional; file will close when `file` goes out of scope
    std::cout << fb << std::endl;
}

void get_positions()
{
    for( TNatural r = 0; r < fb.height( ); ++r )
    {
      for( TNatural c = 0; c < fb.width( ); ++c )
      {
          if ( fb(r, c, 0) == 1)
          {
              
          }
      }
    }
}


void set_dims(std::string line)
{
    std::istringstream iss(line);
    iss >> height >> weight;
    std::cout << "height "<< height << std::endl;
    std::cout << "weight "<< weight << std::endl;
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
      for( TNatural i = 0; i < 3; ++i )
        fb( r, c, i ) = 0;
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
  if(col == 0)
    ++start_col;
  if(row == bottom_edge)
    --end_row;
  if(col == end_col)
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
//          neighbours_on += fb.buffer();
        }
      }
    }
  }
  return neighbours_on;
}

void life_game(FrameBuffer& fb)
{
  
  for( TNatural r = 0; r < fb.height( ); ++r )
  {
    for( TNatural c = 0; c < fb.width( ); ++c )
    {
        //std::cout << fb[c,r]<< std::endl;
    }
  }

}

// eof - simple_color_fill.cxx
