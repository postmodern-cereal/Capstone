#ifndef WORLD_H
#define WORLD_H
#include <vector>
#include "OPair.h"

class World
{
	std::vector<vector<char>> grid;
	int agentX;
	int agentY;
	void setAgentPos(int newX, int newY);

public:
	World(int agentX, int agentY, string fileName = "sample.txt");
	std::<vector<OPair>> getNeighbors(int x, int y);
	void display();


};

#endif
