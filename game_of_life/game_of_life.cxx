// =========================================================================
// @author Leonardo florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <cmath>
#include <iostream>
#include "FrameBuffer.h"
#include <fstream>
#include <string>
#include <sstream>
#include <set>

// -------------------------------------------------------------------------
using TNatural = FrameBuffer::TNatural;
using TReal    = FrameBuffer::TReal;

int height = 0;
int weight = 0;
FrameBuffer fb;
std::set<std::pair<int, int>> initial_positions;
std::set<std::pair<int, int>> positions;
std::set<std::pair<int, int>> positions_to_on;

// -------------------------------------------------------------------------
void fill_framebuffer( FrameBuffer& fb, const TReal* c0, const TReal* c1 );
void read_file(std::string path);
void set_dims(std::string line);
void set_cells_to_evaluate(FrameBuffer& fb);
void evaluate_new_cells(FrameBuffer& fb);
void fill_new_buffer(FrameBuffer& fb);
void set_neighbours_positions( FrameBuffer& fb, const TNatural row, const TNatural col);
FrameBuffer::TBool is_on( FrameBuffer& fb, const TNatural x, const TNatural y );
FrameBuffer::TBool should_turn_on( FrameBuffer& fb, const TNatural x, const TNatural y );
FrameBuffer::TNatural count_neighbours_on( FrameBuffer& fb, const TNatural row, const TNatural col);
void savePBM(const std::string& filename, int width, int height, FrameBuffer& fb);
// -------------------------------------------------------------------------
int main( int argc, char** argv )
{

  TReal c0[ 3 ] = { 1, 0, 1 };
  TReal c1[ 3 ] = { 0, 1, 0 };

//  fb.allocate( 10, 10 );
  //fill_framebuffer( fb, c0, c1 );

//  std::cout << fb << std::endl;
  
    
  std::string path = argv[1];
  int time = std::stoi(argv[2]);
  int fps = std::stoi(argv[3]);
    
  std::cout << " path " << path << std::endl;
  std::cout << " time " << time << std::endl;
  std::cout << " fps " << fps << std::endl;
  int images_qty = time * fps;
  read_file(path);
  for (int i = 0; i < images_qty; ++i)
  {
      if (i > 1)
      {
          initial_positions.clear();
          initial_positions = positions_to_on;
      }
      positions.clear();
      positions_to_on.clear();
      std::cout << std::string(50, '=') << std::endl;
      set_cells_to_evaluate( fb );
      evaluate_new_cells( fb);
      fill_new_buffer( fb );
//      std::cout << fb << std::endl;
      std::cout << std::string(50, '=') << std::endl;
      savePBM("./output/imagen" + std::to_string(i)+".pbm", fb.width(), fb.height(), fb);
  }
//  std::cout << fb << std::endl;

  return( EXIT_SUCCESS );
}

void savePBM(const std::string& filename, int width, int height, FrameBuffer& fb)
{
    std::ofstream file(filename);
    if (!file) {
        std::cerr << "Cannot open file: " << filename << std::endl;
        return;
    }

    file << "P1\n";
    file << width << " " << height << "\n";

    for (int row = 0; row < height; ++row) {
        for (int col = 0; col < width; ++col) {
            if(*fb(row,col) ==  1)
                std::cout << "value 1 " << *fb(row,col) << row <<"--"<<  col<<std::endl;
            file << ((*fb(row, col) != 0) ? "1 " : "0 ");
        }
        file << "\n";
    }

    file.close();
    std::cout << "Saved PBM file: " << filename << std::endl;
}
//
void read_file(std::string path)
{
    std::ifstream file(path);  // open file for reading
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
                    initial_positions.insert({i - 3, j});
                }
                fb( i - 3, j, 0 ) = value;
                j++;
            }
        }
        i++;
    }

    file.close();  // optional; file will close when `file` goes out of scope
    std::cout << fb << std::endl;
}


void set_dims(std::string line)
{
    std::istringstream iss(line);
    iss >> height >> weight;
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

void set_cells_to_evaluate( FrameBuffer& fb )
{
    for (const auto& [row, col] : initial_positions) {
        set_neighbours_positions( fb, row, col);
    }
}

void fill_new_buffer( FrameBuffer& fb)
{
    std::pair<int, int> target;
    for( TNatural r = 0; r < fb.height( ); ++r )
    {
      for( TNatural c = 0; c < fb.width( ); ++c )
      {
        int value = 0;
        target = {r, c};
        if (positions_to_on.find(target) != positions_to_on.end()) {
            value = 1;
        }
        fb( r, c, 0 ) = value;
      } // end for
    }
}

void evaluate_new_cells(FrameBuffer& fb)
{
    for (const auto& [row, col] : positions) {
        if( should_turn_on(fb, row, col) ){
            positions_to_on.insert({row, col});
        }
    }
}



void set_neighbours_positions( FrameBuffer& fb, const TNatural row, const TNatural col)
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
    for(TNatural i = start_row; i < end_row; ++i)
    {
      for(TNatural j = start_col; j < end_col; ++j)
      {
          positions.insert({i,j});
      }
    }
    
}



FrameBuffer::
TBool should_turn_on( FrameBuffer& fb, const TNatural x, const TNatural y )
{
  FrameBuffer::TBool is_born = false;
  TNatural neighbours_on = count_neighbours_on( fb, x, y);
  //neighbours_on 2 or 3
  if((is_on(fb, x, y) && (neighbours_on > 1 && neighbours_on < 4)) ||
     (!is_on(fb, x, y) && count_neighbours_on( fb, x, y) == 3))
  {
    is_born = true; // Cell is born
  }
  return is_born;
}

FrameBuffer::
TNatural count_neighbours_on( FrameBuffer& fb, const TNatural row, const TNatural col)
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
  for(TNatural i = start_row; i < end_row; ++i)
  {
    for(TNatural j = start_col; j < end_col; ++j)
    {
      if((i != row || j != col) && is_on(fb, i, j))
      {
          ++neighbours_on;
      }
    }
  }
  return neighbours_on;
}

FrameBuffer::
TBool is_on( FrameBuffer& fb, const TNatural x, const TNatural y )
{
  FrameBuffer::TBool is_on = false;
    
  if(*fb(x, y) != 0){
      is_on = true;
  }
  return is_on;
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
