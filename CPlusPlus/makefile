CC = g++
OBJ = bar.o
SOURCE = source/
HEADERS = headers/
CFLAGS = -c -Wall -Iheaders
bar: bar.o foo.o
	$(CC) bar.o foo.o -o bar.out
bar.o: src/bar.cpp headers/foo.h
	$(CC) $(CFLAGS) src/bar.cpp -c -g
foo.o: src/foo.cpp headers/foo.h
	$(CC) $(CFLAGS) src/foo.cpp -c -g

clean:
	rm *.o *.out
