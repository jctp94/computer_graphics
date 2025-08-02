## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

all: simple_color_fill

SRCS=simple_color_fill.cxx FrameBuffer.cxx
OBJS=$(SRCS:.cxx=.o)

CXX=g++
CFLAGS=-std=c++20
LDFLAGS=

simple_color_fill: $(OBJS)
	$(CXX) $(LDFLAGS) $^ -o $@

%.o: %.cxx
	$(CXX) $(CFLAGS) -c $^

clean:
	rm -rf simple_color_fill *.o

## eof - Makefile
