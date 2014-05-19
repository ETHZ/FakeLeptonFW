#ifndef CLOSURE_HH
#define CLOSURE_HH

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
#include "TPaletteAxis.h"

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
#include "include/FakeRatios.hh"
#include "Utilities.hh"

#include "include/Fakerates.hh"

// class Closure: public FWBaseClass{
class Closure: public Fakerates{

public:
	Closure();
	Closure(TString, TString);
	virtual ~Closure();

	virtual void init(TString); // Careful, MakeClass produces Init with capital I!

	template <class T> inline void getObjectSafe(TFile* pFile, TString name, T*& object){
		pFile->GetObject(name, object);
		if(!object){
			std::cout << name + " not found!" << std::endl;
			exit(-1);
		}
		return;
	};

	TString fOutputSubDir;
	inline void setVerbose      (int     v) {fVerbose      = v;};
	inline void setData         (bool    d) {fIsData       = d;};
	inline void setInputFile    (TString i) {fInputFile    = i;};
	inline void setOutputDir    (TString o) {fOutputDir    = o;};
	inline void setName         (TString n) {fName         = n;};
	inline void setMaxSize      (int     m) {fMaxSize      = m;};
	inline void setXS           (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};
	inline void setFRFile(TString infile){ fFRFileString = infile;};

	int     fVerbose;
	bool    fIsData;
	TString fOutputDir;
	TString fInputFile;
	TString fName;
	int     fMaxSize;
	float   fXSec;
	float   fLuminosity;

// COUNTERS
	int fTot;
	int fSS;
	int fOS;
	int fSSmm;
	int fSSem;
	int fSSee;
	int fOSmm;
	int fOSem;
	int fOSee;


// INPUT FR FILE
	TString   fFRFileString;
	TFile   * fFRFile;
// INPUT FR HISTOGRAMS
	TH2F    * f_h_FR_data_el;
	TH2F    * f_h_FR_data_mu;
	TH2F    * f_h_FR_data_pure_el;
	TH2F    * f_h_FR_data_pure_mu;
	TH2F    * f_h_FR_mc_el;
	TH2F    * f_h_FR_mc_mu;
	TH2F    * f_h_FR_qcd_el;
	TH2F    * f_h_FR_qcd_mu;
	TH2F    * f_h_FR_ttbar_el;
	TH2F    * f_h_FR_ttbar_mu;

	FakeRatios * fFR;
	float getFRatio(int, float, float);
	void  storePredictions();
	
// FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(TFile*);

	bool isSameSignLLEvent(int&, int&, int&);
	bool passMllCut(int, int, int, float);

// Eventweight
	float fEventWeight;

// OUTPUT TREE

	void bookClosureTree();
	void writeClosureTree(TFile *);
	void resetClosureTree();
	void fillClosureTree();

	TTree * fClosureTree;

	TString  fCT_sname;

	int   fCT_run;
	int   fCT_ls;
	int   fCT_event;
	int   fCT_type;

	float fCT_lumiW;

	float fCT_f1;
	float fCT_f2;
	float fCT_p1;
	float fCT_p2;

	float fCT_npp;
	float fCT_npf;
	float fCT_nfp;
	float fCT_nff;
	int   fCT_tlcat;

	float fCT_pt1;
	float fCT_pt2;
	float fCT_eta1;
	float fCT_eta2;
	float fCT_phi1;
	float fCT_phi2;
	float fCT_iso1;
	float fCT_iso2;
	int   fCT_ch1;

	float fCT_dptrel;
	float fCT_deltas;
	float fCT_lproj;
	float fCT_drl;

	int   fCT_nj;
	int   fCT_nb;
	float fCT_ht;
	float fCT_met;


private:
	
};


#endif
