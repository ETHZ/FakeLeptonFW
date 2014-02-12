#ifndef FAKERATES_HH
#define FAKERATES_HH

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

#include "include/FWBaseClass.h"
#include "Utilities.hh"

class Fakerates: public FWBaseClass{

public:
	Fakerates();
	virtual ~Fakerates();

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
	inline virtual void setData(bool d){ fIsData = d;};
	inline virtual void setInputFile(TString f){ fInputFile = f;};
	inline virtual void setOutputDir(TString d){ fOutputDir = d;};
	inline virtual void setXS(float x){ if(!fIsData) fXSec = x; else fXSec = -1.;};

	int  fVerbose;
	bool fIsData;
	float fXSec;
	TString fInputFile;
	TString fOutputDir;
	

// FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop();

	//void fillRatios();
	void fillIsoPlots();

	bool isCalibrationRegionMuEvent();
	bool isCalibrationRegionElEvent();

	// ===================================
	// the ratio histograms, those are just divided versions of the following
	TH2F * elFRatio;
	TH2F * muFRatio;
	TH2F * elPRatio;
	TH2F * muPRatio;
	
	// passing histograms for electrons and muons, f and p rate
	TH2F * elFPass;
	TH2F * muFPass;
	TH2F * elPPass;
	TH2F * muPPass;

	// failing histograms for electrons and muons, f and p rate
	TH2F * elFFail;
	TH2F * muFFail;
	TH2F * elPFail;
	TH2F * muPFail;

	TH1F * muIsoPlot;
	TH1F * elIsoPlot;

	// ===================================


// SAMPLE CLASS
	class Sample{
		public:
			// Sample(){};
			Sample(TString name, float xs){
				xsec = xs;
				sname = name;
			};
			~Sample(){};
			float xsec;
			TString sname;

	};

private:
	
};


#endif
