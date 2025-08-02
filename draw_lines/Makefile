## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

all: mis_lineas

SRCS=draw_lines.cxx FrameBuffer.cxx
OBJS=$(SRCS:.cxx=.o)

CXX=g++
CFLAGS=-std=c++20
LDFLAGS=

mis_lineas: $(OBJS)
	$(CXX) $(LDFLAGS) $^ -o $@

%.o: %.cxx
	$(CXX) $(CFLAGS) -c $^

clean:
	rm -rf mis_lineas *.o

## eof - Makefile
