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

	cout << "+++++++++++++++++++++++++++++++++++++++++++++++++++++++" << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;
	cout << " Starting Fakerates ...                                " << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;

	TString inputfile    = "";
	TString configfile   = "";
	TString name         = "";
	int verbose          = 0;
	bool isdata          = true;
	float xsec           = 1.;
	int maxsize          = 0;

	// Parse options
	char ch;
	while ((ch = getopt(argc, argv, "i:n:v:x:m:sn:c:h:?")) != -1 ) {
		switch (ch) {
			case 'i': inputfile    = TString(optarg)       ;  break;
			case 'n': name         = TString(optarg)       ;  break;
			case 'v': verbose      = atoi(optarg)          ;  break;
			case 's': isdata       = false                 ;  break;
			case 'c': configfile   = TString(optarg)       ;  break;
			case 'x': xsec         = atof(optarg)          ;  break; //::atof( ((std::string) optarg).c_str());  break;
			case 'm': maxsize      = atoi(optarg)          ;  break;
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

	cout << " verbose level is:   " << verbose     << endl;
	cout << " config file is:     " << configfile  << endl;
	cout << " inputfile is:       " << inputfile   << endl;
	cout << " name is:            " << name        << endl;
	cout << " running on " << (isdata?"data":"mc") << endl;
	cout << " xsec is:            " << xsec        << endl;
	cout << " sample max size is: " << maxsize     << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;

	Fakerates *frA = new Fakerates(configfile);
	frA->setVerbose(verbose);
	frA->setData(isdata);
	frA->setXS(xsec);
	frA->setInputFile(inputfile);
	frA->setName(name);
	frA->setMaxSize(maxsize);
	frA->doStuff();
	// delete frA;
	
	cout << " done ...                                              " << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;
	cout << "......................................................." << endl;

	return 0;
}

