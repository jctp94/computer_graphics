## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

all: game_of_life

SRCS=game_of_life.cxx FrameBuffer.cxx
OBJS=$(SRCS:.cxx=.o)

CXX=g++
CFLAGS=-std=c++20
LDFLAGS=

game_of_life: $(OBJS)
	$(CXX) $(LDFLAGS) $^ -o $@

%.o: %.cxx
	$(CXX) $(CFLAGS) -c $^

clean:
	rm -rf game_of_life *.o

## eof - Makefile
