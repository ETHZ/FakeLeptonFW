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

	inline virtual void setVerbose   (int     v) {fVerbose   = v;};
	inline virtual void setData      (bool    d) {fIsData    = d;};
	inline virtual void setInputFile (TString f) {fInputFile = f;};
	inline virtual void setOutputDir (TString d) {fOutputDir = d;};
	inline virtual void setName      (TString n) {fName      = n;};
	inline virtual void setXS        (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};

	int  fVerbose;
	bool fIsData;
	float fXSec;
	TString fInputFile;
	TString fOutputDir;
	TString fOutputFilename;
	TString fName;
	

// FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop();

	//void fillRatios();
	void fillIsoPlots();

	void synchOutput();
	
	bool passesUpperMETMT(int, int);

	bool isCalibrationRegionMuEvent(int&);
	bool isCalibrationRegionElEvent(int&);

	bool isGoodJet(int, float);
	bool isGoodSynchJet(int, float);

	std::vector<float>::const_iterator fITFloat;
	std::vector<bool >::const_iterator fITBool;
	std::vector< int >::const_iterator fITInt;

	// ===================================
	// the ratio histograms, those are just divided versions of the following
	TH2F * h_elFRatio;
	TH2F * h_muFRatio;
	TH2F * h_elPRatio;
	TH2F * h_muPRatio;
	
	// passing histograms for electrons and muons, f and p rate
	TH2F * h_elFTight;
	TH2F * h_muFTight;
	TH2F * h_elPTight;
	TH2F * h_muPTight;

	// failing histograms for electrons and muons, f and p rate
	TH2F * h_elFLoose;
	TH2F * h_muFLoose;
	TH2F * h_elPLoose;
	TH2F * h_muPLoose;

	TH1F * h_muIsoPlot;
	TH1F * h_elIsoPlot;

	TH1F * h_muD0Plot;
	TH1F * h_elD0Plot;

	void bookHistos();
	void writeHistos(TFile *);

	// ===================================

	int fCutflow_afterLepSel;
	int fCutflow_afterJetSel;
	int fCutflow_afterMETCut;
	int fCutflow_afterMTCut ;
	

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
