#ifndef ESTIMATION_HH
#define ESTIMATION_HH

#include "TMath.h"

#include "TString.h"
#include "TObject.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TH1.h"
#include "TH2.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TRandom.h"
#include "TROOT.h"
#include "TVirtualPad.h"
#include "TLorentzVector.h"

#include "TPaveStats.h"

#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>
#include <vector>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <time.h> // access to date/time

#include "TreeClass.h"
#include "Utilities.hh"

class Estimation: public TreeClass{

public:
	Estimation();
	virtual ~Estimation();

	virtual void init(bool = false); // Careful, MakeClass produces Init with capital I!

	template <class T> inline void getObjectSafe(TFile* pFile, TString name, T*& object){
		pFile->GetObject(name, object);
		if(!object){
			std::cout << name + " not found!" << std::endl;
			exit(-1);
		}
		return;
	};

	TString fOutputSubDir;
	inline virtual void setVerbose(int v){ fVerbose = v;};

	int fVerbose;
	
// FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(const char *);

private:
	
};


#endif
