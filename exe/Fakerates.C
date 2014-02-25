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
	bool isdata(true);
	TString name = "";
	float xsec(1.);
    int maxsize(0);

	// Parse options
	char ch;
	while ((ch = getopt(argc, argv, "i:o:v:x:m:sn:h?")) != -1 ) {
		switch (ch) {
			case 'i': inputfile  = TString(optarg)       ;  break;
			case 'o': outputdir  = TString(optarg)       ;  break;
			case 'v': verbose    = atoi(optarg)          ;  break;
			case 's': isdata     = false                 ;  break;
			case 'n': name       = TString(optarg)       ;  break;
			case 'x': xsec       = ::atof( ((std::string) optarg).c_str());  break;
            case 'm': maxsize    = atoi(optarg)          ;  break;
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

	cout << "------------------------------------" << endl;
	cout << " verbose level is:  " << verbose << endl;
	cout << " inputfile is:      " << inputfile << endl;
	cout << " outputdir is:      " << outputdir << endl;
	cout << " running on " << (isdata?"data":"mc") << endl;
	cout << " xsec: " << xsec << endl;
    cout << " sample max size " << maxsize << endl;
	cout << " sample name " << name << endl;

	Fakerates *frA = new Fakerates();
	frA->setVerbose(verbose);
	frA->setData(isdata);
	frA->setXS(xsec);
	frA->setInputFile(inputfile);
	frA->setOutputDir(outputdir);
    frA->setMaxSize(maxsize);
	frA->setName(name);
	frA->doStuff();
	// delete frA;
	cout << "...done" << endl;
	return 0;
}

