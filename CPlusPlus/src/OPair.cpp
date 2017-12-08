#include "OPair.h"
#include <stdlib.h>

OPair::OPair(int x, int y, char type)
{
	this->x = x;
	this->y = y;
	this->type = type;
}

int OPair::getX()
{
	return x;
}


int OPair::getY()
{
	return Y;
}


char OPair::getType()
{
	return type;
}

int OPair::distance(OPair other)
{
	return (abs(getX() - other.getX()) + (getY() - other.getY());
}
