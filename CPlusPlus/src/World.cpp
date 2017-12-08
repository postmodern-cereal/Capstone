#include <iostream>
#include <fstream>
#include <vector>
#include "World.h"

using namespace std;

World::World(int agentX, int agentY, string fileName = "sample.txt")
{
	this.setAgentPos(agentX, agentY);
	//now we need to get world data from the file
	//step 1: make sure that the file exists. If it does not, we will use a default file
	fstream file(fileName, fstream::in);
	if(file.is_open())
	{
		//file opened successfully, so read the stuff
		int width = -1;
		int length;
		char c;
		string s;
		while(file >> noskipws >> c)
		{
			
		}

	}
}

void World::setAgentPos(int newX, int newY)
{
	this->agentX = newX;
	this->agentY = newY;
}
