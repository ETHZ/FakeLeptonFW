// C++ includes
#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>

// ROOT includes
#include <TROOT.h>
#include "TString.h"

#include "include/Closure.hh"

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
	TString frfile  = "";
	TString inputfile  = "";
	TString outputdir  = "";
	TString configfile = "";
	int verbose        = 0;
	bool isdata        = true;
	int maxsize        = 0;

	// Parse options
	char ch;
	while ((ch = getopt(argc, argv, "i:v:x:n:m:o:c:r:h?")) != -1 ) {
		switch (ch) {
			case 'i': inputfile  = TString(optarg);  break;
			case 'r': frfile     = TString(optarg);  break;
			case 'o': outputdir  = TString(optarg);  break;
			case 'c': configfile = TString(optarg);  break;
			case 'v': verbose    = atoi(optarg);     break;
			case 'm': maxsize      = atoi(optarg);   break;
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
	if(verbose > 0) cout << " FR Inputfile is:   " << inputfile << endl;
	if(verbose > 0) cout << " Outputdir is:      " << outputdir << endl;
	if(verbose > 0) cout << " inputfile is:       " << inputfile   << endl;
	if(verbose > 0) cout << " running on " << (isdata?"data":"mc") << endl;
	if(verbose > 0) cout << " sample max size is: " << maxsize     << endl;
	if(verbose > 0) cout << "=======================================================" << endl;
	if(verbose > 0) cout << "=======================================================" << endl;

	Closure *clA = new Closure(frfile, configfile);

	std::pair<TString , float> nameXSec = clA->getNameAndXsec(inputfile);

	clA->setName(nameXSec.first);
	clA->setXS(nameXSec.second);
	std::cout << "Running on sample " << nameXSec.first << " with a cross section of " << nameXSec.second << " pb." << std::endl;

	clA->setVerbose(verbose);
	clA->setFRFile(frfile);
	clA->setInputFile(inputfile);
	clA->setOutputDir(outputdir);
	clA->setMaxSize(maxsize);
	clA->doStuff();

	// delete clA;
	return 0;
}

