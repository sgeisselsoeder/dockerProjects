#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

int main()
{
	std::ifstream inHere("./input/dummyInput.txt");
	assert(inHere.is_open() && inHere.good());
	std::ofstream outOfHere("outputfile.txt");
	assert(outOfHere.is_open() && outOfHere.good());

	std::string temp;
	inHere >> temp;
	while (inHere.good())
	{
		std::cout << "I've read entry " << temp << std::endl;
		outOfHere << temp << std::endl;
		inHere >> temp;
	}
	inHere.close();
	outOfHere.close();
	return 0;	
}
