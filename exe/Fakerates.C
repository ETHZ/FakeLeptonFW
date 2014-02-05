// C++ includes
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

// ROOT includes
#include <TROOT.h>
#include "TString.h"

#include "include/Fakerates.hh"

using namespace std;

//_____________________________________________________________________________________
// Print out usage
void usage( int status = 0 ) {
	cout << "Usage: foobar" << endl;
	cout << endl;
	exit(status);
}

//_____________________________________________________________________________________
int main(int argc, char* argv[]) {
	TString inputfile  = "";
	TString outputdir  = "";
	int verbose(0);

	// Parse options
	char ch;
	while ((ch = getopt(argc, argv, "i:v:h?")) != -1 ) {
		switch (ch) {
			case 'i': inputfile  = TString(optarg);  break;
			case 'o': outputdir  = TString(optarg);  break;
			case 'v': verbose    = atoi(optarg);     break;
			case '?':
			case 'h': usage(0); break;
			default:
			cerr << "*** Error: unknown option " << optarg << std::endl;
			usage(-1);
		}
	}

	// Check arguments
	if( argc<1 ) {
		usage(-1);
	}

	if(verbose > 0) cout << "------------------------------------" << endl;
	if(verbose > 0) cout << " Verbose level is:  " << verbose << endl;
	if(verbose > 0) cout << " Inputfile is:      " << inputfile << endl;
	if(verbose > 0) cout << " Outputdir is:      " << outputdir << endl;

	Fakerates *frA = new Fakerates();
	frA->setVerbose(verbose);
	frA->doStuff();
	delete frA;
	return 0;
}

