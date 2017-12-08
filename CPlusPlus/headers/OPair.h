#ifndef OPAIR_H
#define OPAIR_H

//a class for coordinates. useful sort of.

class OPair
{
private:
	int x;
	int y;
	char type;

public:
	OPair(int x, int y, char type);
	int getX();
	int getY();
	int getType();
	int distance(OPair other);
};

#endif
